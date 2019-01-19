#!/usr/bin/env python

from PyRM import PyRM, Config

# Let's run this thing!
for i in range(10):
	config = Config.ConfigDrumBullySlow()
	pyrm = PyRM.PyRM(config)
	pyrm.buildTrack()
	pyrm.writeFile(str(i))



#for i in range(5):
#	config = PadConfigLow()
	#pyrm = PyRM(config)
	#pyrm.buildTrack()
	#pyrm.writeFile(str(i))

	
	
#for i in range(10):
#	config = BullyDrumFastConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))

#	config = BullyDrumSlowConfig()
#	pyrm = PyRM(config)
#	pyrm.buildTrack()
#	pyrm.writeFile(str(i))

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
