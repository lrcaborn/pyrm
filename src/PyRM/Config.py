#!/usr/bin/env python

from enum import Enum
import lea

	
# MIDI NOTES
# 21-32 A0-G#0
# 33-44 A1-G#1
# 45-56 A2-G#2
# 57-68 A3-G#3
# 69-80 A4-G#4
# 81-92 A5-G#5
# 93-104 A6-G#6
# 105-116 A7-G#0
# 117-128 A8-G#8

# CHANCE int to percentage likelihood
# 1 = 100% chance
# 2 = 50% 
# 3 = 33% 
# 4 = 25%
# 5 = 20%
# 10 = 10%
# 20 = 5%
# 50 = 2%
# 100 = 1%

class NoteConfig:
	categories = {}
	count_scope = []
	forbidden_notes = {}
	length_scope = []
	max_simultaneous = 0
	scope = []
	simultaneous_chance = 1
	simultaneous_chance_scope = []
	span_scope = []
	ticks_per_quarternote = 480 #960
	
class TempoConfig:
	pass

class ConfigBase:
	name = "Base"
	debug_log = True
	chooser = None
	use_randomized_tuning = False

	volume_scope = [1, 127]

	note_config = NoteConfig()
	#note_config.ticks_per_quarternote = 480 #960
	note_config.count_scope = [100, 1000]
	note_config.length_scope = [1, note_config.ticks_per_quarternote*4]
	note_config.max_simultaneous = 3
	note_config.simultaneous_chance = 4
	note_config.simultaneous_chance_scope = [1, 100]
	note_config.scope = [21, 108] # A0 to C8
	
	tempo_scope = [30, 200]
	tempo_change_chance_range = [1, 100]
	tempo_change_chance = 2

	@classmethod
	def getStats(self):
		print(self.chooser)

	
	
class ConfigBass(ConfigBase):
	name = "Bass"

	note_config = ConfigBase.note_config
	note_config.length_scope = [100, 200]


class ConfigBassSlow(ConfigBass):
	name = "Bass Slow"
	
	tempo_scope = [60, 90]
	volume_scope = [90, 100]

	note_config = ConfigBass.note_config
	#note_config.count_scope = config.count_scope
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [1, note_config.ticks_per_quarternote*2]
	#note_config.length_scope = [100, 200]
	note_config.max_simultaneous = 3
	note_config.scope = [26, 60]
	#note_config.simultaneous_chance = config.simultaneous_chance
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope



class ConfigBassFast(ConfigBass):
	name = "Bass Fast"
	
	tempo_scope = [150, 180]
	volume_scope = [90, 110]
	
	note_config = ConfigBass.note_config
	#note_config.count_scope = config.count_scope
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [1, note_config.ticks_per_quarternote]
	#note_config.length_scope = [100, 200]
	note_config.max_simultaneous = 2
	note_config.scope = [26, 48]
	#note_config.simultaneous_chance = config.simultaneous_chance
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope

	
	
class ConfigDrum(ConfigBase):
	name = "Drum"
	
	note_config = ConfigBase.note_config
	note_config.length_scope = [100, 200]
	note_config.max_simultaneous = 3

	
	
# 16 Bully Hats Open4
# 17-20
# 21 Bully Hats Pedal Closed
# 22 Bully Hats Closed Edge
# 23 Bully Hats Pedal Open
# 24 Bully Hats Open1
# 25 Bully Hats Open2
# 26 Bully Hats Open3
# 27 Bully Crash Cymbal1
# 28 Bully China Cymbal1
# 29 Bully Crash Cymbal3
# 30 Bully Spock Cymbal
# 31 Bully Crash Cymbal4
# 32 Bully Crash Cymbal6
# 32-34
# 36 Bully Kick Drum
# 37 Bully Snare Sidestick
# 38 Bully Snare Center Hits
# 39 Bully Snare Center Hits
# 40 Bully Snare Rimshots
# 41 Bully Floor Tom2
# 42 Bully Hats Closed Tip
# 43 Bully Floor Tom1
# 44 Bully Hats Pedal Closed
# 45 Bully Rack Tom2
# 46 Bully Hats Open2
# 47 Bully Rack Tom2
# 48 Bully Rack Tom1
# 49 Bully Crash Cymbal2
# 50 Bully Rack Tom1-D
# 51 Bully Ride Cymbal Tip
# 52 Bully China Cymbal2
# 53 Bully Ride Cymbal Bell
# 54 Bully Cowbell Tip
# 55 Bully Splash Cymbal
# 56 Bully Cowbell Edge
# 57 Bully Crash Cymbal5
# 58 
# 59 Bully Ride Cymbal Crash
# 60 Bully Hats Open5
# 61 
# 62 Bully Hats Tight Edge
# 63 Bully Hats Tight Tip
# 64 Bully Hats Open 0
# 65 Bully Hats Sequenced Hits


class ConfigDrumBully(ConfigDrum):
	name = "BullyDrum"

	class Category(Enum):
		KICK = "Kick"
		SNARE = "Snare"
		HAT = "Hi-Hat"
		CYMBAL_CRASHES = "Cymbal Crashes"
		TOM = "Toms"
		RIDE_CYMBAL = "Ride cymbal"
		COWBELL = "Cowbell"

		def __str__(self):
			return self.name

	note_config = ConfigDrum.note_config
	note_config.categories = {
		Category.HAT.value: [16,21,22,23,24,25,26,42,44,46,60,62,63,64,65],
		Category.CYMBAL_CRASHES.value: [27,28,29,30,31,32,49,52,55,57,59],
		Category.KICK.value: [36],
		Category.SNARE.value: [37,38,39,40],
		Category.TOM.value: [41,43,45,47,48,50],
		Category.RIDE_CYMBAL.value: [51,53],
		Category.COWBELL.value: [54,56]
	}
	#note_config.count_scope = note_config.count_scope
	note_config.forbidden_notes = {17,18,19,20,33,34,35,58,61}
	#note_config.length_scope = note_config.length_scope
	#note_config.max_simultaneous = note_config.max_simultaneous
	note_config.scope = list(set(range(16, 65)) - note_config.forbidden_notes)
	note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = note_config.simultaneous_chance_scope
	#note_config.span_scope = note_config.span_scope

	volume_scope = [90, 127]

	ConfigDrum.chooser = lea.pmf({
		Category.COWBELL.value: 0.05,
		Category.CYMBAL_CRASHES.value: 0,
		Category.HAT.value: 0.15,
		Category.KICK.value: 0.30,
		Category.RIDE_CYMBAL.value: 0.15,
		Category.SNARE.value: 0.25,
		Category.TOM.value: 0.10
	})

class ConfigDrumBullySlow(ConfigDrumBully):
	name = "BullyDrumSlow"

	note_config = ConfigDrumBully.note_config
	note_config.length_scope = [note_config.ticks_per_quarternote/8, note_config.ticks_per_quarternote]
	note_config.count_scope = [100,100]

	tempo_scope = [40, 70]

class ConfigDrumBullyFast(ConfigDrumBully):
	name = "BullyDrumFast"

	note_config = ConfigDrumBully.note_config
	note_config.length_scope = [note_config.ticks_per_quarternote/2, note_config.ticks_per_quarternote]
	note_config.count_scope = [1000,1500]

	tempo_scope = [150, 180]
	
	
class ConfigDrumEzxJazz(ConfigDrum):
	name = "EzxJazz"

	class Category(Enum):
		HAT = "Hi-Hat"
		KICK = "Kick"
		RIDE = "Ride cymbal"
		SNARE = "Snare"
		CRASH = "Cymbal Crashes"
		TOM = "Toms"
		
		def __str__(self):
			return self.name

	note_config = ConfigDrum.note_config
	note_config.categories = {
		Category.HAT.value: [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,42,44,46,60,61,62,63,64,65,119,120,121,122,123,124],
		Category.KICK.value: [34,35,36],
		Category.RIDE.value: [30,31,32,51,52,53,57,58,59,84,85,86,87,88,89,90,91,92,93,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118],
		Category.SNARE.value: [6,33,37,38,39,40,66,67,68,69,70,71,125,126,127],
		Category.CRASH.value: [27,28,29,49,54,55,83,94,95],
		Category.TOM.value: [4,5,41,43,45,47,48,50,72,73,74,75,77,78,79,80,81,82]
	}
	#note_config.count_scope = note_config.count_scope
	note_config.forbidden_notes = {1,2,3,56,76}
	#note_config.length_scope = note_config.length_scope
	#note_config.max_simultaneous = note_config.max_simultaneous
	note_config.scope = list(set(range(0, 128)) - note_config.forbidden_notes)
	note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = note_config.simultaneous_chance_scope
	#note_config.span_scope = note_config.span_scope			

	# skip 0 so we avoid division by 0 errors
	start_time_factors = tuple(range(-1, 0)) + tuple(range(1, 11))

	ConfigDrum.chooser = lea.pmf({
		Category.CRASH.value: 0,
		Category.HAT.value: 0.15,
		Category.KICK.value: 0.25,
		Category.RIDE.value: 0.15,
		Category.SNARE.value: 0.25,
		Category.TOM.value: 0.15
	})	

class ConfigDrumEzxJazzSlow(ConfigDrumEzxJazz):
	name = "EzxJazzSlow"
	
	note_config = ConfigDrumEzxJazz.note_config
	#note_config.categories = config.categories
	note_config.count_scope = [50,100]
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [note_config.ticks_per_quarternote, note_config.ticks_per_quarternote*2]
	#note_config.max_simultaneous = 3
	#note_config.scope = list(set(range(0, 128)) - forbidden_notes)
	#note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope			
	
	tempo_scope = [40, 70]
	
class ConfigDrumEzxJazzFast(ConfigDrumEzxJazz):
	name = "EzxJazzFast"
	
	note_config = ConfigDrumEzxJazz.note_config
	#note_config.categories = config.categories
	note_config.count_scope = [100,150]
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [note_config.ticks_per_quarternote, note_config.ticks_per_quarternote*2]
	#note_config.max_simultaneous = 3
	#note_config.scope = list(set(range(0, 128)) - forbidden_notes)
	#note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope			

	tempo_scope = [150, 200]
	
class ConfigOrnament(ConfigBase):
	name = "Ornament"

	note_config = ConfigBase.note_config
	#note_config.categories = config.categories
	note_config.count_scope = [100,1000]
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [note_config.ticks_per_quarternote/4, note_config.ticks_per_quarternote]
	note_config.max_simultaneous = 4
	note_config.scope = [0, 127]
	#note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope			

	volume_scope = [80, 100]
	tempo_scope = [30, 300]

class ConfigOrnamentPiano(ConfigOrnament):
	name = "OrnamentPiano"

	class Category(Enum):
		LOW = "Low"
		HIGH = "High"
		
		def __str__(self):
			return self.name
	
	note_config = ConfigOrnament.note_config
	note_config.scope = [21, 109]
	note_config.categories = {
		Category.LOW.value: list(range(note_config.scope[0], 45)),
		Category.HIGH.value: list(range(46, note_config.scope[1]))
	}
	note_config.count_scope = [10, 25]
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [note_config.ticks_per_quarternote/4, note_config.ticks_per_quarternote]
	note_config.max_simultaneous = 4
	#note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope
	
	volume_scope = [80, 100]
	tempo_scope = [100, 150]

	start_time_factors = tuple(range(1, 5))

	ConfigOrnament.chooser = lea.pmf({
		Category.LOW.value: 0.25,
		Category.HIGH.value: 0.75,
	})

class ConfigPadPiano(ConfigBase):
	name = "Pad Piano"

	class Category(Enum):
		LOW = "Low"
		MIDDLE = "Middle"
		HIGH = "High"
		
		def __str__(self):
			return self.name
	
	note_config = ConfigBase.note_config
	note_config.scope = [21, 109]
	note_config.categories = {
		Category.LOW.value: list(range(note_config.scope[0], 60)),
		Category.MIDDLE.value: list(range(61, 70)),
		Category.HIGH.value: list(range(71, note_config.scope[1]))
	}
	note_config.count_scope = [10, 15]
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [note_config.ticks_per_quarternote, note_config.ticks_per_quarternote*4]
	note_config.max_simultaneous = 3
	note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope
	
	volume_scope = [80, 100]
	tempo_scope = [150, 200]
	
	ConfigBase.chooser = lea.pmf({
		Category.LOW.value: 0.025,
		Category.MIDDLE.value: 0.95,
		Category.HIGH.value: 0.025,
	})

class ConfigCompPiano(ConfigBase):
	name = "Comp Piano"
	
	class Category(Enum):
		LOW = "Low"
		MIDDLE = "Middle"
		HIGH = "High"
		
		def __str__(self):
			return self.name
	
	note_config = ConfigBase.note_config
	note_config.scope = [21, 109]
	note_config.categories = {
		Category.LOW.value: list(range(note_config.scope[0], 60)),
		Category.MIDDLE.value: list(range(61, 70)),
		Category.HIGH.value: list(range(71, note_config.scope[1]))
	}
	note_config.count_scope = [10, 15]
	#note_config.forbidden_notes = config.forbidden_notes
	note_config.length_scope = [note_config.ticks_per_quarternote/2, note_config.ticks_per_quarternote*2]
	note_config.max_simultaneous = 3
	note_config.simultaneous_chance = 2
	#note_config.simultaneous_chance_scope = config.simultaneous_chance_scope
	#note_config.span_scope = config.span_scope
	
	tempo_scope = [80, 120]
	volume_scope = [80, 100]

	ConfigBase.chooser = lea.pmf({
		Category.LOW.value: 0.025,
		Category.MIDDLE.value: 0.95,
		Category.HIGH.value: 0.025,
	})
	