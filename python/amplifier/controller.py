from amplifier.pt2314 import PT2314
from amplifier.i2c import I2cInit
from amplifier.radio import Radio
from amplifier.mp3 import Mp3
from time import sleep
import json
import os

# Amplifier Controller v2.0
#
# Accepts messages that affect the state of the system
#
# web server -> incoming
# input thread -> incoming
# i2cAmplifier <- outgoing
# i2cRadio <- outgoing
# mp3 <- outgoing
#
# Ronald Diaz 2015
# ronald@ronalddiaz.net
#
# Messages ::
#
# Inputs:
#       -> PowerOn
#       -> PowerOff
#       -> MuteOn
#       -> MuteOff
#       -> MuteToggle
#       -> SelectMedia
#       -> SelectMusic
#       -> SelectRadio
#       -> SelectAux
#       -> SelectToggle
#       -> VolumeUp
#       -> VolumeDown
#       -> VolumeSet(0 -> 100)
#       -> VolumeDelta(-x -> x)
#
# MPD Commands
# isPlaying
# getSong
# getSongTimeRemain
# getSongTimeTotal
#
# Radio Commands
# switch station
#
class Controller():
  def __init__(self):
    
    # Amplifier States
    self.muteState = False
    self.powerState = False
    self.selectState = 0 # 0 -> 3
    
    # Volume 0->100
    self.volume = 50
    self.volumei2c = 0x20

    # Tone
    self.bass = 0
    self.treble = 0

    # reset i2c ports
    self.i = I2cInit()
    
    # i2c PT2314 Resource
    self.audio = PT2314()

    # i2c Radio Resource
    self.radio = Radio()

    # mpd control Resource
    self.mp3 = Mp3()

    # PT2314 channel mapping
    self.channelMedia = 0
    self.channelAux   = 1
    self.channelMusic = 2
    self.channelRadio = 3

    self.powerOn()

  # json formatted ok response
  def ok(self, status = "ok"):
    data = {"result" : True, "status" : status}
    return json.dumps(data)
  
  # Power On
  #
  def powerOn(self):
    # if self.powerState == True:
    #   return self.ok("ok. Power already on.")
    self.powerState = True
    self.volumeSet(50)
    self.audio.loudnessOn()
    self.muteOff()
    self.selectMedia()
    self.audio.setAttenuation(0,0)
    self.audio.setBass(0)
    self.audio.setTreble(0)
    self.radio.setStationIndex(0)
    return self.getAll()

  # Power Off
  #
  def powerOff(self):
    self.powerState = False
    self.audio.powerOff()
    os.system("poweroff")
    return self.ok("shutting down")

  # Select Audio Input [ Media | Aux | Radio | Music ]
  #
  def selectMedia(self):
    self.audio.selectChannel(self.channelMedia)
    self.selectState = self.channelMedia
    return self.getAll()

  def selectMusic(self):
    self.audio.selectChannel(self.channelMusic)
    self.selectState = self.channelMusic
    return self.getAll()

  def selectRadio(self):
    self.audio.selectChannel(self.channelRadio)
    self.selectState = self.channelRadio
    return self.getAll()

  def selectAux(self):
    self.audio.selectChannel(self.channelAux)
    self.selectState = self.channelAux
    return self.getAll()

  def selectToggle(self):
    # toggle through states
    self.selectState = self.selectState + 1
    # upper limit
    if self.selectState > 3:
      self.selectState = 0
    # switch states
    if self.selectState == self.channelMedia:
      self.selectMedia()
    elif self.selectState == self.channelAux:
      self.selectAux()
    elif self.selectState == self.channelMusic:
      self.selectMusic()
    elif self.selectState == self.channelRadio:
      self.selectRadio()
    return self.getAll()

  def muteOn(self):
    self.audio.muteOn()
    self.muteState = True
    return self.getAll()

  def muteOff(self):
    if self.muteState == False:
      return self.ok("ok. Mute already off.")
    self.audio.muteOff()
    self.muteState = False
    return self.getAll()

  def muteToggle(self):
    #print "mute toggle: currently: " + str(self.muteState)
    if self.muteState == False:
      self.muteOn()
    else:
      self.muteOff()
    return self.getAll()

  # Volume Methods
  #
  def volumeUp(self):
    self.volume = self.volumeValidate(self.volume + 1)
    self.audio.setVolume(self.volumei2c)
    return self.getAll()

  def volumeDown(self):
    self.volume = self.volumeValidate(self.volume - 1)
    self.audio.setVolume(self.volumei2c)
    return self.getAll()

  def volumeDelta(self, delta=0):
    if delta == 0:
      return self.ok("ok. no volume change")
    delta = int(delta)
    self.volume = int(self.volumeValidate(int(self.volume) + (delta / 2)))
    self.audio.setVolume(self.volumei2c)
    return self.getAll()

  def volumeSet(self, volume):
    self.volume = self.volumeValidate(volume)
    #print "controller:volume:" + str(self.volume)
    self.audio.setVolume(self.volumei2c)
    return self.getAll()
      
  def volumeValidate(self, vol):
    #print "controller:volumeValidate:" + str(vol)
    if vol == '':
     vol = 0
    vol = int(vol)
    if vol<0:
      vol=0
    if vol>100:
      vol=100
    #print "controller:volumeValidate:post:" + str(vol)
    # calculate audio i2c volume
    self.volumei2c = int(0x3F - float((float(63)/float(100) * float(vol))))
    return vol

  # Tone Methods
  #
  def bassSet(self, bass):
    self.bass = self.audio.setBass(bass)
    return self.getAll()

  def trebleSet(self, treble):
    self.treble = self.audio.setTreble(treble)
    return self.getAll()

  def bassUp(self):
    return self.bassSet(self.bass + 2)

  def bassDown(self):
    return self.bassSet(self.bass - 2)

  def trebleUp(self):
    return self.trebleSet(self.treble + 2)

  def trebleDown(self):
    return self.trebleSet(self.treble - 2)

  # Radio Methods
  #
  def radioStationPrevious(self):
    self.radio.prevStation()
    return self.getAll()

  def radioStationNext(self):
    self.radio.nextStation()
    return self.getAll()

  def radioStationIndex(self, index):
    self.radio.setStationIndex(index)
    return self.getAll()

  # Mp3 Methods
  #
  def mp3Previous(self):
    self.mp3.previous()
    return self.getAll()

  def mp3Next(self):
    self.mp3.next()
    return self.getAll()

  def mp3Pause(self):
    self.mp3.pause()
    return self.getAll()

  def mp3Stop(self):
    self.mp3.stop()
    return self.getAll()

  def mp3Play(self):
    self.mp3.play()
    return self.getAll()

  def mp3SeekForward(self):
    self.mp3.seekForward()
    return self.getAll()

  def mp3SeekBackward(self):
    self.mp3.seekBackward()
    return self.getAll()

  # Getters
  #
  def volumeGet(self):
    return self.volume

  def getStateString(self):
    if self.selectState == self.channelMedia:
      return 'media'
    elif self.selectState == self.channelAux:
      return 'aux'
    elif self.selectState == self.channelMusic:
      return 'music'
    elif self.selectState == self.channelRadio:
      return 'radio'

  def getAll(self):
    data = {
            'power'   : self.powerState,
            'state'   : self.getStateString(),
            'volume'  : self.volume,
            'mute'    : self.muteState,
            'select'  : self.selectState,
            'bass'    : self.bass,
            'treble'  : self.treble,
            'radio'   : self.radio.getStation(),
            'mp3'     : self.mp3.getStatus()
           }
    return json.dumps(data)
