#!/usr/bin/env python
import json
import lea
import random
import uuid

from midiutil import MIDIFile

# TODO
# * change config to json?
# * note categories
#   * assign probabilities per category so, e.g., cymbals happen less often than drums

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

class BaseConfig:
	TICKS_PER_QUARTERNOTE = 960
	name = "Base"
	note_length_range = [1, TICKS_PER_QUARTERNOTE*4]
	volume_range = [1, 127]
	pitch_range = [21, 108] # A0 to C8
	tempo_range = [30, 200]
	note_count_range = [100, 1000]
	use_randomized_tuning = False
	tempo_change_chance_range = [1, 100]
	tempo_change_chance = 2
	maximum_simultaneous_notes = 3
	simultaneous_notes_chance_range = [1, 100]
	simultaneous_notes_chance = 4
	excluded_notes = []
	unpairable_notes = {}

class PadConfig(BaseConfig):
	name = "Pad"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE*8]
	volume_range = [80, 100]
	pitch_range = [21, 108] # A0 to C8
	tempo_range = [60, 80]
	note_count_range = [500, 750]
	maximum_simultaneous_notes = 5

class PadConfigLow(PadConfig):
	name = "Pad Low"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE*8]
	volume_range = [80, 100]
	pitch_range = [21, 45] # A0 to C8
	tempo_range = [60, 80]
	note_count_range = [500, 750]
	maximum_simultaneous_notes = 3
	
class OrnamentConfig(BaseConfig):
	name = "Ornament"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE]
	volume_range = [30, 100]
	pitch_range = [21, 108] # A0 to C8
	tempo_range = [30, 999]
	note_count_range = [100, 1000]
	maximum_simultaneous_notes = 4

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

class DrumConfig(BaseConfig):
	name = "Drum"

class KitCoreMtDillConfig(BaseConfig):
	name = "Kit-Core Mt Dill"
	pitch_range = [24, 39]
	maximum_simultaneous_notes = 4
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE/2]
	tempo_range = [150, 180]
	volume_range = [90, 127]
	note_count_range = [500, 1000]

class BullyDrumConfig(DrumConfig):
	name = "BullyDrum"
	pitch_range = [16, 65]
	excluded_notes = [17,18,19,20,32,34,35,58,61]

	# defaults to being unpairable with own note
	unpairable_notes = {
		16: [21,22,23,24,25,26,42,44,46,60,62,63,64,65],
		21: [16,22,23,24,25,26,42,44,46,60,62,63,64,65],
		22: [16,21,23,24,25,26,42,44,46,60,62,63,64,65],
		23: [16,21,22,24,25,26,42,44,46,60,62,63,64,65],
		24: [16,21,22,23,25,26,42,44,46,60,62,63,64,65],
		25: [16,21,22,23,24,26,42,44,46,60,62,63,64,65],
		26: [16,21,22,23,24,25,42,44,46,60,62,63,64,65],
		36: [37,38,39,40],
		37: [36,38,39,40],
		38: [36,37,39,40],
		39: [36,37,38,40],
		40: [36,37,38,39],
		42: [16,21,22,23,24,25,26,44,46,60,62,63,64,65],
		44: [16,21,22,23,24,25,26,42,46,60,62,63,64,65],
		45: [37],
		46: [16,21,22,23,24,25,26,42,44,60,62,63,64,65],
		47: [45],
		48: [50],
		50: [48],
		51: [53,59],
		53: [51,59],
		59: [51,53],
		60: [16,21,22,23,24,25,26,42,44,46,62,63,64,65],
		62: [16,21,22,23,24,25,26,42,44,46,60,63,64,65],
		63: [16,21,22,23,24,25,26,42,44,46,60,62,64,65],
		64: [16,21,22,23,24,25,26,42,44,46,60,62,63,65],
		65: [16,21,22,23,24,25,26,42,44,46,60,62,63,64]
	}

# CHANCE int to percentage likelihood
# 1 = 100% chance
# 2 = 50% 
# 3 = 33%
# 4 = 25%
# 5 = 20%
# 6 = 15%
# 7 = 14%
# 8 = 12%
# 9 = 11%
# 10 = 10%
# 20 = 5%
# 50 = 2%
# 100 = 1%

	note_categories = {
		"Hats": { 6: [16,21,22,23,24,25,26,42,44,46,60,62,63,64,65] },
		"Cymbal Crashes": {6: [27,28,29,30,31,32,49,52,55,57,59]},
		"Kick": {5: [36]},
		"Snare": {5: [37,38,39,40]},
		"Toms": {6: [41,43,45,47,48,50]},
		"Ride cymbal": {10: [51,53] },
		"Cowbell": {20: [54,56] }
	}






	
class BullyDrumSlowConfig(BullyDrumConfig):
	name = "BullyDrumSlow"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE]
	tempo_range = [60, 90]
	volume_range = [90, 110]
	note_count_range = [100,200]
	
class BassSlowConfig(BaseConfig):
	name = "Bass Slow"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE*2]
	volume_range = [90, 100]
	pitch_range = [26, 60]
	tempo_range = [60, 90]
	note_count_range = [100, 200]
	maximum_simultaneous_notes = 3

class BullyDrumFastConfig(BullyDrumConfig):
	name = "BullyDrumFast"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE/2]
	tempo_range = [150, 180]
	volume_range = [90, 127]
	note_count_range = [100,200]

class BassFastConfig(BaseConfig):
	name = "Bass Fast"
	note_length_range = [1, BaseConfig.TICKS_PER_QUARTERNOTE]
	volume_range = [90, 110]
	pitch_range = [26, 48]
	tempo_range = [150, 180]
	note_count_range = [100, 200]
	maximum_simultaneous_notes = 2


class Application:
	config = None
	midi = None
	
	@classmethod
	def __loadConfig(self, config):
		print("using " + config.name + " configuration")
		self.config = config

	@classmethod
	def __init__(self, config):
		self.__loadConfig(config)
		self.midi = MIDIFile(1, deinterleave = False, eventtime_is_ticks = True, ticks_per_quarternote = config.TICKS_PER_QUARTERNOTE)

	@classmethod
	def __frequency(self, midi_note):
		"""Calculate frequency of given midi note"""
		return 27.5 * 2 ** ((midi_note - 21)/12)

	@staticmethod
	def __greaterOf(first, second):
		if first > second:
			return first
		else:
			return second

	@staticmethod
	def __lesserOf(first, second):
		if first < second:
			return first
		else:
			return second

	@staticmethod
	def __getRandomFromRange(range):
		return random.randint(range[0], range[1])

	@classmethod
	def __generateRandomizedTuning(self):
		if self.config.use_randomized_tuning == True:
			base_tuning = []
			new_tuning = []

			for count, note in enumerate(range(128)):
				base_tuning.append(self.config.frequency(note))

			for count, frequency in enumerate(base_tuning):
				if count == 0:
					tuning = (count, random.uniform(base_tuning[count], base_tuning[count + 1]))
				elif count == len(base_tuning) - 1:
					tuning = (count, random.uniform(base_tuning[count - 1], base_tuning[count]))
				else:
					tuning = (count, random.uniform(base_tuning[count - 1], base_tuning[count + 1]))
				new_tuning.append(tuning)

			for count, value in enumerate(base_tuning):
				print(value, " ", new_tuning[count])

			self.midi.changeNoteTuning(0, new_tuning, tuningProgam=0)

	@classmethod
	def __generatePitch(self):
		pitch = self.__getRandomFromRange(self.config.pitch_range)
		while pitch in config.excluded_notes:
			pitch = self.__getRandomFromRange(self.config.pitch_range)
		return pitch

	@classmethod
	def buildTrack(self):
		channel = 0
		track = 0
		note_start_time = 0
		note_count = self.__getRandomFromRange(self.config.note_count_range)
		degrees = range(0, note_count, 1)

		tempo = self.__getRandomFromRange(self.config.tempo_range)
		self.midi.addTempo(track, note_start_time, tempo)

		for i in enumerate(degrees):
			volume = self.__getRandomFromRange(self.config.volume_range)
			note_length = self.__getRandomFromRange(self.config.note_length_range)
			pitch = self.__generatePitch()
			tempo_change_chance = self.__getRandomFromRange(self.config.tempo_change_chance_range)

			if tempo_change_chance % self.config.tempo_change_chance == 0:
				tempo = self.__getRandomFromRange(self.config.tempo_range)
			
			self.midi.addNote(track, channel, pitch, note_start_time, note_length, volume)
			
			original_pitch = pitch
			for j in range(self.config.maximum_simultaneous_notes):
				simultaneous_note_chance = self.__getRandomFromRange(self.config.simultaneous_notes_chance_range)
				if simultaneous_note_chance % self.config.simultaneous_notes_chance == 0:
					pitch = self.__generatePitch()
					if pitch == original_pitch or (original_pitch in self.config.unpairable_notes and pitch in self.config.unpairable_notes[original_pitch]):
						break
					else:
						self.midi.addNote(track, channel, pitch, note_start_time, note_length, volume)

			# determine next note_start_time so that we always start the track with the first note @ 0
			note_start_time = note_start_time + self.__getRandomFromRange(self.config.note_length_range)
			
	@classmethod
	def writeFile(self, customIdentifier):
		id = customIdentifier
		if id == "":
			id += "."
		filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".mid"
			
		with open(filename, "wb") as output_file:
			self.midi.writeFile(output_file)

# Let's run this thing!
for i in range(5):
	config = PadConfigLow()
	app = Application(config)
	app.buildTrack()
	app.writeFile(str(i))

#for i in range(10):
	#config = BullyDrumFastConfig()
#	app = Application(config)
	#app.buildTrack()
	#app.writeFile(str(i))
#
#	config = BassFastConfig()
#	app = Application(config)
#	app.buildTrack()
#	app.writeFile(str(i))
#
#	config = OrnamentConfig()
#	app = Application(config)
#	app.buildTrack()
#	app.writeFile(str(i))
#
#for i in range(9):
	#config = BullyDrumSlowConfig()
	#app = Application(config)
	#app.buildTrack()
	#app.writeFile(str(i))
#
#	config = BassSlowConfig()
#	app = Application(config)
#	app.buildTrack()
#	app.writeFile(str(i))
#
#	config = PadConfig()
#	app = Application(config)
#	app.buildTrack()
#	app.writeFile(str(i))
