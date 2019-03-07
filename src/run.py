#!/usr/bin/env python

from PyRM import PyRM, Config

for i in range(1):
	config = Config.ConfigDrumEzxJazzMid()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.convertTrackToMidi()
	midiFile = pyrm.exportMidiFile(str(i))
	jsonFile = pyrm.exportTrackToJsonFile(str(i))
	
