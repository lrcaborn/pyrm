#!/usr/bin/env python

from PyRM import PyRM, Config

# Let's run this thing!
#for i in range(1):
#	config = Config.ConfigDrumBullySlow()
#	pyrm = PyRM.PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeStats()
#	pyrm.writeFile(str(i))


#for i in range(5):
#	config = Config.ConfigDrumBullyFast()
#	pyrm = PyRM.PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeStats()
#	pyrm.writeFile(str(i))

#for i in range(5):
#	config = Config.ConfigDrumEzxJazzSlow()
#	print (config.note_scope)
#	pyrm = PyRM.PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))
#	pyrm.writeStats()
#	pyrm.writeLog()

	
	
for i in range(5):
	config = Config.ConfigPad()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.writeFile(str(i))
	pyrm.writeStats()
	pyrm.writeLog()

	
	
#for i in range(10):
#	config = BullyDrumFastConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))
#
#	config = BullyDrumSlowConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))
#
#	config = BassFastConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))

#	config = OrnamentConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))

#for i in range(9):
#	config = BullyDrumSlowConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))

#	config = BassSlowConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))

#	config = PadConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))
