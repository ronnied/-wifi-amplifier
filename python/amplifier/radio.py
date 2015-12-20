import subprocess
from configobj import ConfigObj

######################################
#
# Class for controlling FM TEA65767
# through an installed c application
#
# Ronald Diaz ronald@ronalddiaz.net
#
class Radio:
  def __init__(self):
    self.stationIdx = 0    # 
    self.station = {}      # current station
    self.stations = {}     # all stations
    self._readConfig()     # read config

  # High Level Methods

  def prevStation(self):
    if(self.stationIdx == 0):
      self.stationIdx = (len(self.stations) - 1)
    else:
      self.stationIdx = self.stationIdx - 1
    self.setStationIndex(self.stationIdx)

  def nextStation(self):
    if(self.stationIdx == (len(self.stations) - 1)):
      self.stationIdx = 0
    else:
      self.stationIdx = self.stationIdx + 1
    self.setStationIndex(self.stationIdx)

  def setStationIndex(self, index):
    self.station = self.stations[str(index)]
    #print "setStationIndex: ", index, str(index)
    self._updateStation()

  def getStation(self):
    return self.station

  # Low Level Methods

  def _readConfig(self):
    # open config file
    self.config = ConfigObj("/root/config-radio")
    
    # read all the stations
    self.stations = self.config['stations']

    # read default station
    defaultIdx = self.config['default']

    # set default station
    self.station = self.config['stations'][defaultIdx]

  def _updateStation(self):
    # print "Set Station: ", self.station
    # Get frequency of this station
    frequency = self.station['frequency']

    # Use subprocess to call radio application
    subprocess.call(['/usr/bin/radio', str(frequency)])
