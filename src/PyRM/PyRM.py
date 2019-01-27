#!/usr/bin/env python
import json
import lea
import logging
import random
import uuid

from midiutil import MIDIFile

# TODO
# map ezdrummer kits

class PyRM:
	config = None
	midi = None
	categories = None
	
#################
# CLASS METHODS #
#################
	@classmethod
	def __init__(self, config):
		logging.basicConfig(filename='debug.log',level=logging.DEBUG)
		self.__loadConfig(config)
		self.midi = MIDIFile(1, deinterleave = False, eventtime_is_ticks = True, ticks_per_quarternote = config.TICKS_PER_QUARTERNOTE)

	@classmethod
	def __loadConfig(self, config):
		self.config = config
		config_info = "using " + config.name + " configuration"
		self.__logDebug(config_info)

	@classmethod
	def __frequency(self, midi_note):
		"""Calculate frequency of given midi note"""
		return 27.5 * 2 ** ((midi_note - 21)/12)

	@classmethod
	def __generatePitch(self):
		try:
			category = self.config.chooser.random()
			range = self.config.note_categories[category]
			self.__logDebug("category: " + str(category) + " range: " + str(range))
		except AttributeError:
			range = self.config.allowed_notes

		pitch = self.__getRandom(range)
		return pitch

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
				self.__logDebug(value, " ", new_tuning[count])

			self.midi.changeNoteTuning(0, new_tuning, tuningProgam=0)

	@classmethod
	def buildTrack(self):
		channel = 0
		track = 0
		note_start_time = 0

		note_count = self.__getRandom(self.config.note_count_scope)
		# generates tuple of categories that will match up reasonably well with 
		# the probabilities specified when defining the chooser in the config
		self.categories = self.config.chooser.random(note_count)
		
		self.__logDebug("start generating track")
		
		tempo = self.__getRandom(self.config.tempo_scope)
		self.midi.addTempo(track, note_start_time, tempo)
		self.__logDebug("TEMPO: " + str(track) + " " + str(note_start_time) + " " + str(tempo))

		self.__logDebug("category	pitch	note_start_time	note_length	volume")
		for i,category in enumerate(self.categories):
			volume = self.__getRandom(self.config.volume_scope)
			note_length = self.__getRandom(self.config.note_length_scope)
			
			self.__logDebug("category: " + category)
			
			pitch = self.config.note_categories[category][self.__getRandom(len(self.config.note_categories[category]))]
			#self.__logDebug("pitch " + str(pitch) + " selected from range " + str(self.config.note_categories[category]))

			################
			# TEMPO CHANGE #
			################
			tempo_change_chance = self.__getRandom(self.config.tempo_change_chance_range)
			if tempo_change_chance % self.config.tempo_change_chance == 0:
				tempo = self.__getRandom(self.config.tempo_scope)
				self.midi.addTempo(track, note_start_time, tempo)
				self.__logDebug("TEMPO: " + str(track) + " " + str(note_start_time) + " " + str(tempo))
			
			self.midi.addNote(track, channel, pitch, note_start_time, note_length, volume)
			self.__logDebug("NOTE: " + str(category) + "	" + str(pitch) + "	" + str(note_start_time) + "	" + str(note_length) + "	" + str(volume))
			
			######################
			# SIMULTANEOUS NOTES #
			######################
			simultaneous_pitches = [pitch]
			for j in range(self.config.maximum_simultaneous_notes):

				simultaneous_note_chance = self.__getRandom(self.config.simultaneous_note_chance_scope)
				if simultaneous_note_chance % self.config.simultaneous_notes_chance == 0:

					found_valid_pitch = False
					while found_valid_pitch == False:
						# getting a pitch for a simultaneous note doesn't need to be limited by the category
						pitch = self.config.allowed_notes[self.__getRandom(len(self.config.allowed_notes))]

						if pitch in simultaneous_pitches: 
							# we don't want to add notes already used to the list of simultaneous pitches
							self.__logDebug("SIM NOTE failure: " + str(pitch) + " already used: " + str(simultaneous_pitches))
							break
						elif (pitch in self.config.note_categories[category]):
							# we don't want to add notes that are unpairable with the first note
							self.__logDebug("SIM NOTE failure: pitch " + str(pitch) + " is in the current category " + str(self.config.note_categories[category]))
							break
						elif (simultaneous_pitches[0] in self.config.unpairable_notes and pitch in self.config.unpairable_notes[simultaneous_pitches[0]]):
							# we don't want to add notes that are unpairable with the first note
							self.__logDebug("SIM NOTE failure: simultaneous_pitches[0] " + str(simultaneous_pitches[0]) + " unpairable with " + str(pitch))
							break
						else:
							found_valid_pitch = True
							self.midi.addNote(track, channel, pitch, note_start_time, note_length, volume)
							self.__logDebug("SIM NOTE: " + str(category) + " " + str(pitch) + " " + str(note_start_time) + " " + str(note_length) + " " + str(volume))
				else:
					break

			# determine next note_start_time after adding the first note
			# so that we always start the track with the first note @ 0
			note_start_time = note_start_time + int(self.__getRandom(self.config.note_length_scope) / 2)

	@classmethod
	def writeFile(self, customIdentifier):
		id = customIdentifier
		if id == "":
			id += "."
		filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".mid"
			
		with open(filename, "wb") as output_file:
			self.midi.writeFile(output_file)
			
	@classmethod
	def writeStats(self):
		self.__logDebug(self.config.getStats())
		self.__logDebug(lea.vals(*self.categories))


##################
# STATIC METHODS #
##################

	@staticmethod
	def __getRandom(*args):
		if (len(args) == 1):
			if (isinstance(args[0], int)):
				return random.randrange(args[0])
			elif (isinstance(args[0], list)) and (len(args[0]) == 2):
				if (args[0][0] == args[0][1]):
					return args[0][0];
				else:
					return random.randrange(args[0][0], args[0][1])
		else:
			self.__logDebug(str(args))

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
	def __logDebug(message):
		#logging.debug(message)
		print(message)
