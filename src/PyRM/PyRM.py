#!/usr/bin/env python
import json
import random
import uuid

from midiutil import MIDIFile

# TODO
# map ezdrummer kits

class PyRM:
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
		if len(range) == 1:
			return range[0]
		else:
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
		try:
			category = self.config.chooser.random()
			range = self.config.note_categories[category]
		except AttributeError:
			range = self.config.pitch_range

		pitch = self.__getRandomFromRange(range)
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
