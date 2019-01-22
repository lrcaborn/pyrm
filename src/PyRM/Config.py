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

class ConfigBase:
	TICKS_PER_QUARTERNOTE = 480 #960
	name = "Base"
	note_length_scope = [1, TICKS_PER_QUARTERNOTE*4]
	volume_scope = [1, 127]
	allowed_notes = [21, 108] # A0 to C8
	tempo_scope = [30, 200]
	note_count_scope = [100, 1000]
	use_randomized_tuning = False
	tempo_change_chance_range = [1, 100]
	tempo_change_chance = 2
	maximum_simultaneous_notes = 3
	simultaneous_note_chance_scope = [1, 100]
	simultaneous_notes_chance = 4
	forbidden_notes = []
	unpairable_notes = {}
	debug_log = True
	
	chooser = None
	
	@classmethod
	def getStats(self):
		print(self.chooser)

	
	
class ConfigBass(ConfigBase):
	pass

class ConfigBassSlow(ConfigBass):
	name = "Bass Slow"
	note_length_scope = [1, ConfigBass.TICKS_PER_QUARTERNOTE*2]
	volume_scope = [90, 100]
	allowed_notes = [26, 60]
	tempo_scope = [60, 90]
	note_count_scope = [100, 200]
	maximum_simultaneous_notes = 3

class ConfigBassFast(ConfigBass):
	name = "Bass Fast"
	note_length_scope = [1, ConfigBass.TICKS_PER_QUARTERNOTE]
	volume_scope = [90, 110]
	allowed_notes = [26, 48]
	tempo_scope = [150, 180]
	note_count_scope = [100, 200]
	maximum_simultaneous_notes = 2
	
	
	
class ConfigDrum(ConfigBase):
	name = "Drum"

	
	
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
	class Category(Enum):
		KICK = "Kick"
		SNARE = "Snare"
		HATS = "Hats"
		CYMBAL_CRASHES = "Cymbal Crashes"
		TOMS = "Toms"
		RIDE_CYMBAL = "Ride cymbal"
		COWBELL = "Cowbell"
		LOW = "Low"
		HIGH = "High"
		
#		def __str__(self):
#			return str(self.value)

	volume_scope = [90, 127]

	maximum_simultaneous_notes = 3
	simultaneous_notes_chance = 2

	name = "BullyDrum"
	forbidden_notes = {17,18,19,20,33,34,35,58,61}
	allowed_notes = list(set(range(16, 65)) - forbidden_notes)
	
	# defaults to being unpairable with own note
	unpairable_notes = {
		16: [21,22,23,24,25,26,42,44,46,60,62,63,64,65],
		21: [16,22,23,24,25,26,42,44,46,60,62,63,64,65],
		22: [16,21,23,24,25,26,42,44,46,60,62,63,64,65],
		23: [16,21,22,24,25,26,42,44,46,60,62,63,64,65],
		24: [16,21,22,23,25,26,42,44,46,60,62,63,64,65],
		25: [16,21,22,23,24,26,42,44,46,60,62,63,64,65],
		26: [16,21,22,23,24,25,42,44,46,60,62,63,64,65],
		42: [16,21,22,23,24,25,26,44,46,60,62,63,64,65],
		44: [16,21,22,23,24,25,26,42,46,60,62,63,64,65],
		46: [16,21,22,23,24,25,26,42,44,60,62,63,64,65],
		60: [16,21,22,23,24,25,26,42,44,46,62,63,64,65],
		62: [16,21,22,23,24,25,26,42,44,46,60,63,64,65],
		63: [16,21,22,23,24,25,26,42,44,46,60,62,64,65],
		64: [16,21,22,23,24,25,26,42,44,46,60,62,63,65],
		65: [16,21,22,23,24,25,26,42,44,46,60,62,63,64],

		37: [38,39,40],
		38: [37,39,40],
		39: [37,38,40],
		40: [37,38,39],

		45: [37],
		47: [45],
		48: [50],
		50: [48],

		51: [53,59],
		53: [51,59],
		59: [51,53]
	}

	note_categories = {
		Category.HATS: [16,21,22,23,24,25,26,42,44,46,60,62,63,64,65],
		Category.CYMBAL_CRASHES: [27,28,29,30,31,32,49,52,55,57,59],
		Category.KICK: [36],
		Category.SNARE: [37,38,39,40],
		Category.TOMS: [41,43,45,47,48,50],
		Category.RIDE_CYMBAL: [51,53],
		Category.COWBELL: [54,56]
	}

	ConfigDrum.chooser = lea.pmf({
		Category.COWBELL: 0.05,
		Category.CYMBAL_CRASHES: 0,
		Category.HATS: 0.15,
		Category.KICK: 0.30,
		Category.RIDE_CYMBAL: 0.15,
		Category.SNARE: 0.25,
		Category.TOMS: 0.10
	})

class ConfigDrumBullySlow(ConfigDrumBully):
	name = "BullyDrumSlow"
	note_length_scope = [ConfigBase.TICKS_PER_QUARTERNOTE/8, ConfigBase.TICKS_PER_QUARTERNOTE]
	tempo_scope = [40, 70]
	note_count_scope = [900,1000]

class ConfigDrumBullyFast(ConfigDrumBully):
	name = "BullyDrumFast"
	note_length_scope = [1, ConfigBase.TICKS_PER_QUARTERNOTE/2]
	tempo_scope = [150, 180]
	note_count_scope = [2500,3000]

	
	
	
	
class ConfigDrumKitCoreMtDill(ConfigDrum):
	name = "Kit-Core Mt Dill"
	allowed_notes = [24, 39]
	maximum_simultaneous_notes = 4
	note_length_scope = [1, ConfigBase.TICKS_PER_QUARTERNOTE/2]
	tempo_scope = [150, 180]
	volume_scope = [90, 127]
	note_count_scope = [500, 1000]

	
	
	
	
class ConfigOrnament(ConfigBase):
	name = "Ornament"
	note_length_scope = [1, ConfigBase.TICKS_PER_QUARTERNOTE]
	volume_scope = [30, 100]
	allowed_notes = [21, 108] # A0 to C8
	tempo_scope = [30, 999]
	note_count_scope = [100, 1000]
	maximum_simultaneous_notes = 4

	
	
	
	
class ConfigPad(ConfigBase):
	name = "Pad"
	note_length_scope = [1, ConfigBase.TICKS_PER_QUARTERNOTE*8]
	volume_scope = [80, 100]
	allowed_notes = [21, 108] # A0 to C8
	tempo_scope = [60, 80]
	note_count_scope = [500, 750]
	maximum_simultaneous_notes = 5

class ConfigPadLow(ConfigPad):
	name = "Pad Low"
	note_length_scope = [1, ConfigBase.TICKS_PER_QUARTERNOTE*8]
	volume_scope = [80, 100]
	allowed_notes = [21, 45] # A0 to C8
	tempo_scope = [60, 80]
	note_count_scope = [500, 750]
	maximum_simultaneous_notes = 3

	
	
	
