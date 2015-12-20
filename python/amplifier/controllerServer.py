from twisted.web.resource import Resource
from amplifier.controller import Controller
# from amplifier.input import Input

# Control Server just delegates
# messages interpreted to the
# Controller Resource
#
class ControllerServer(Resource):

  print "amplifier controller server started"
  isLeaf = True
  
  # Controller Resource
  controller = Controller()
  #controller.powerOn()
  
  # Input Resource - direct connection to Controller object
  # input = Input.Worker(controller)
  # input.start()
  
  def render_GET(self, request):
    request.setHeader("content-type", "application/json")
    return self.translateGET(request)

  def translateGET(self, get):
    path = (get.__dict__)["path"]
    seg = path.split("/")
    #print seg #print seg[1]
    if seg[1] == "set":
      return self.routeSet(seg) 
    elif seg[1] == "get":
      return self.routeGet(seg)
    else:
      return "Error"

  ########################################################  
  # Delegate incoming set  
  def routeSet(self, seg):
    
    # command to switch
    sw = seg[2]
    #print sw
    
    if sw == "muteToggle":
      return self.controller.muteToggle()
    elif sw == "muteOn":
      return self.controller.muteOn()
    elif sw == "muteOff":
      return self.controller.muteOff()
    elif sw == "selectToggle":
      return self.controller.selectToggle()
    elif sw == "selectMedia":
      return self.controller.selectMedia()
    elif sw == "selectMusic":
      return self.controller.selectMusic()
    elif sw == "selectRadio":
      return self.controller.selectRadio()
    elif sw == "selectAux":
      return self.controller.selectAux()
    elif sw == "volume":
      volume = 0
      try:
        volume = seg[3]
      except ValueError:
        volume = 0
      return self.controller.volumeSet(volume)
    elif sw == "volumeDelta":
      delta = 0
      try:
        delta = seg[3]
      except ValueError:
        delta = 0
      return self.controller.volumeDelta(delta)
    elif sw == "powerOn":
      return self.controller.powerOn()
    elif sw == "powerOff":
      return self.controller.powerOff()
    # Tone controls
    elif sw == "bassUp":
      return self.controller.bassUp()
    elif sw == "bassDown":
      return self.controller.bassDown()
    elif sw == "trebleUp":
      return self.controller.trebleUp()
    elif sw == "trebleDown":
      return self.controller.trebleDown()
    elif sw == "bass":
      bass = 0
      try:
        bass = seg[3]
      except ValueError:
        bass = 0
      return self.controller.bassSet(bass)
    elif sw == "treble":
      treble = 0
      try:
        treble = seg[3]
      except ValueError:
        treble = 0
      return self.controller.trebleSet(treble)
    # Radio
    elif sw == "radioStationPrevious":
      return self.controller.radioStationPrevious()
    elif sw == "radioStationNext":
      return self.controller.radioStationNext()
    elif sw == "radioStationIndex":
      station = 0
      try:
        station = seg[3]
      except ValueError:
        station = 0
      return self.controller.radioStationIndex(station)
    # Mp3
    elif sw == "mp3Next":
      return self.controller.mp3Next()
    elif sw == "mp3Previous":
      return self.controller.mp3Previous()
    elif sw == "mp3Stop":
      return self.controller.mp3Stop()
    elif sw == "mp3Play":
      return self.controller.mp3Play()
    elif sw == "mp3Pause":
      return self.controller.mp3Pause()
    elif sw == "mp3SeekForward":
      return self.controller.mp3SeekForward()
    elif sw == "mp3SeekBackward":
      return self.controller.mp3SeekBackward()
    else:
      error = "Unknown command: " + str(sw)
      #print error
      return error

  ########################################################
  # Delegate incoming get    
  def routeGet(self, seg):
    # command to switch
    sw = seg[2]
    #print sw
    
    # High level commands
    #
    if sw == "all":
      return self.controller.getAll()
    elif sw == "status":
      return self.controller.getAll()
    elif sw == "stateString":
      return self.controller.getStateString()
    else:
      msg = "not implemented"
      #print msg
      return msg
