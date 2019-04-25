#!/usr/bin/env python
import pprint
from PyRM import PyRM, Config

for i in range(20):
  config = Config.ConfigPianoLongChords()
  pyrm = PyRM.PyRM(config)
  pyrm.buildTrack()
  
  #pprint.pprint(pyrm.phrases)
  pyrm.convertTrackToMidi()
  midiFile = pyrm.exportMidiFile(str(i))
  jsonFile = pyrm.exportTrackToJsonFile(str(i))
  
