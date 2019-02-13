#!/usr/bin/env python

from PyRM import PyRM, Config

for i in range(25):
	config = Config.ConfigOrnamentPiano()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.writeFile(str(i))
	pyrm.writeStats()
	pyrm.writeLog()

