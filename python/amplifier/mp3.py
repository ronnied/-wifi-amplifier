import mpd
import time

######################################
#
# Class for controlling MPDaemon
#
# Ronald Diaz ronald@ronalddiaz.net
#
# sets: no delay, send request to mpd daemon
# gets: run worker to cache mpd daemon data
# at a regular timely rate, return cache
#
class Mp3:
  def __init__(self):
    self.currentStatus = False
    self.mpd = False
    self.connect()
    self.timer = 0 # always expired to start with
    self.timerLimit = 7500 # in milliseconds
    self.currentTime = lambda: int((round(time.time() * 1000)))
    self.cachedStatus = False
    self.pauseState = True

  # High Level Commands
  def connect(self):
    try:
      self.mpd = mpd.MPDClient()
      self.mpd.timeout = 10
      self.mpd.use_unicode = False
      self.mpd.connect("localhost", 6600)
      # Check response from port is correct: OK MPD 0.17.0
    except:
      self.mpd = False

  def getStatus(self):
    if self.mpd == False:
      return self.currentStatus
    if self._hasCacheExpired() == True:
      return self._getMPDStatus()
    else:
      return self.currentStatus

  def previous(self):
    if self.mpd == False:
      return self.currentStatus
    self.mpd.previous()

  def next(self):
    if self.mpd == False:
      return self.currentStatus
    self.mpd.next()

  def pause(self):
    if self.mpd == False:
      return self.currentStatus
    if self.pauseState == True:
      self.mpd.pause(1)
      self.pauseState = False
    else:
      self.mpd.pause(0)
      self.pauseState = True
  
  def stop(self):
    if self.mpd == False:
      return self.currentStatus
    self.mpd.stop()

  def play(self):
    if self.mpd == False:
      return self.currentStatus
    self.mpd.play()

  def seekForward(self):
    self.mpd.seekcur("+5")

  def seekBackward(self):
    self.mpd.seekcur("-5")

  def _getMPDStatus(self):
    try:
      self.currentStatus = self.mpd.currentsong()
    except:
      return False
    return self.currentStatus

  def _timerReset(self):
    self.timer = self.currentTime()

  def _hasCacheExpired(self):
    if (self.currentTime() - self.timer) > self.timerLimit:
      self._timerReset()
      return True
    else:
      return False
