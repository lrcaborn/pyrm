#!/usr/bin/env python

from PyRM import PyRM, Config

for i in range(10):
	config = Config.ConfigCompPiano()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.writeFile(str(i))
	pyrm.writeStats()
	pyrm.writeLog()

for i in range(10):
	config = Config.ConfigOrnamentPiano()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.writeFile(str(i))
	pyrm.writeStats()
	pyrm.writeLog()
