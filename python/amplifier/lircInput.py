import pylirc
import threading
import time

class LircInput:
  def __init__(self, Controller):
    # Direct connection to the Controller object
    self.controller = Controller
    self.code = None

  # Threaded Worker
  class Worker(threading.Thread):
    def __init__(self, Controller):
      threading.Thread.__init__(self)
      self.lock = threading.Lock()
      self.daemon = True
      self.MAIN_THREAD_DELAY = 0.01
      self.controller = Controller
      try:
        self.sockid = pylirc.init("myamp", "/etc/lirc/lirc.config")
        pylirc.blocking(0)
      except:
        print "error connecting to lircd!"
      self.code = None
      
    def run(self):
      while True:
        self.code = pylirc.nextcode(0)
        if self.code != None or self.code == "None":
          self.handleLircCode(self.code)
        #print self.code
        time.sleep(self.MAIN_THREAD_DELAY)

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
          return self.controller.radioStationNext()
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