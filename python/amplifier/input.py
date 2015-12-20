from amplifier.lircInput import LircInput
import threading
from time import sleep
import sys

class Input:
  def __init__(self, Controller): 

    # LIRC Input
    self.lirc = LircInput.Worker()
    self.lirc.start()

    # Direct connection to the Controller object
    self.controller = Controller

  def handleLircCode(self, code):
    print "got code: " + str(code)
    if code[0] == 'mute':
      return self.controller.muteToggle()
    if code[0] == 'up':
      return self.controller.volumeUp()
    if code[0] == 'down':
      return self.controller.volumeDown()
    if code[0] == 'red':
      return self.controller.selectAux()
    if code[0] == 'green':
      return self.controller.selectMusic()
    if code[0] == 'yellow':
      return self.controller.selectRadio()
    if code[0] == 'blue':
      return self.controller.selectMedia()
    if code[0] == 'stop' and self.controller.getStateString() == "music":
      return self.controller.mp3Stop()
    if code[0] == 'play' and self.controller.getStateString() == "music":
      return self.controller.mp3Play()
    if code[0] == 'pause' and self.controller.getStateString() == "music":
      return self.controller.mp3Pause()
    if code[0] == 'seekForward':
      return self.controller.mp3SeekForward()
    if code[0] == 'seekBackward':
      return self.controller.mp3SeekBackward()
    if code[0] == 'power':
      pass
    if code[0] == 'back':
      selected = self.controller.getStateString()
      if selected == "radio":
        return self.controller.radioStationPrevious()
      if selected == "music":
        return self.controller.mp3Previous()
    if code[0] == 'forward':
      selected = self.controller.getStateString()
      if selected == "radio":
        return sself.controller.radioStationNext()
      if selected == "music":
        return self.controller.mp3Next()
    if code[0] == 'bassDown':
      return self.controller.bassDown()
    if code[0] == 'bassUp':
      return self.controller.bassUp()
    if code[0] == 'trebleDown':
      return self.controller.trebleDown()
    if code[0] == 'trebleUp':
      return self.controller.trebleUp()

  # Threaded Worker
  class Worker(threading.Thread):
    # cache prev state
    # signal on change state
    def __init__(self, Controller = None):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.daemon = True
      
      # Decrease for greater resolution at the cost of cpu cycles
      self.MAIN_THREAD_DELAY = 0.01
      
      # Input resource
      self.input = Input(Controller)
      
    def run(self):
      while True:

        # monitor lirc for changes
        lircCode = self.input.lirc.getCode()
        if lircCode != None or lircCode == "None":
          self.input.handleLircCode(lircCode)

        # sleep...
        sleep(self.MAIN_THREAD_DELAY)