#!/usr/bin/env python

from PyRM import PyRM, Config

for i in range(1):
	config = Config.ConfigPadSynth()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.convertTrackToMidi()
	midiFile = pyrm.exportMidiFile(str(i))
	print("exported midi file: " + midiFile)
	jsonFile = pyrm.exportTrackToJsonFile(str(i))
	print("exported json file: " + jsonFile)
	i += 1


	config2 = Config.ConfigPadSynth()
	pyrm2 = PyRM.PyRM(config2)
	pyrm2.importJsonFileToTrack(jsonFile)
	midiFile = pyrm2.exportMidiFile(str(i))
	pyrm.convertTrackToMidi()
	print("exported midi file: " + midiFile)
	jsonFile = pyrm2.exportTrackToJsonFile(str(i))
	print("exported json file: " + jsonFile)
	
