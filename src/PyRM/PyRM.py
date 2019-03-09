#!/usr/bin/env python
import jsonpickle
import lea
import logging
import random
import uuid

from midiutil import MIDIFile

def jsonDefault(OrderedDict):
    return OrderedDict.__dict__
  
class Note:
  def __init__(self, length = 0, pitch = 0, volume = 0):
    self.length = length
    self.pitch = pitch
    self.volume = volume

  def __repr__(self):
    return "length: " + str(self.length) + " pitch: " + str(self.pitch) + " volume: " + str(self.volume)

    
class Phrase:
  def __init__(self):
    self.chords = dict()

  def addNote(self, start_time, note):
    if (start_time not in self.chords):
        self.chords[start_time] = list()
    
    self.chords[start_time].append(note)

  def __repr__(self):
    return str(self.chords)

class Track:
  def __init__(self):
    # tempos is just key/value. Key = start time and value is the tempo
    self.tempos = dict()
    # notes is key/value with key being start time and value being a list of note objects
    self.notes = dict()
    
  def __repr__(self):
    return jsonpickle.encode(self)
    #return json.dumps(self, default=jsonDefault, indent=4)

class PyRM:
  def __init__(self, config):
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    self.__loadConfig(config)
    self.midi = MIDIFile(1, deinterleave = False, eventtime_is_ticks = True, ticks_per_quarternote = config.note_config.ticks_per_quarternote)
    self.debug_tables = {
      "GENERAL": [],
      "PITCH": [],
      "TEMPO": [],
      "TUNING": []
    }
    self.track = Track()
    self.phrases = list()

  def __loadConfig(self, config):
    self.config = config
    config_info = "using " + config.name + " configuration"

  def __frequency(self, midi_note):
    """Calculate frequency of given midi note"""
    return 27.5 * 2 ** ((midi_note - 21)/12)

  def __generatePitch(self, isPrimaryNote):
    try:
      category = self.config.note_config.chooser.random()
      if isPrimaryNote:
        range = self.config.note_config.categories[category]
        pitch = range[self.__getRandom(len(range))]
        self.__logDebug("PITCH", "HAVE CHOOSER - PRIMARY pitch: " + str(pitch) + " from category: " + str(category) + " with range: " + str(range))
      else:
        range = self.config.note_config.scope
        pitch = self.__getRandom(range)
        self.__logDebug("PITCH", "HAVE CHOOSER - NONPRIMARY pitch: " + str(pitch) + " from category: " + str(category) + " with range: " + str(range))
    except AttributeError:
      range = self.config.note_config.scope
      pitch = self.__getRandom(range)
      self.__logDebug("PITCH", "NO CHOOSER - pitch: " + str(pitch) + " from range: " + str(range))

    return pitch

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
        self.__logDebug("TUNING", value, " ", new_tuning[count])

      self.midi.changeNoteTuning(0, new_tuning, tuningProgam=0)

  def __logDebug(self, debug_table, message):
    self.debug_tables[debug_table].append(message)
    #logging.debug(message)
    #print(message)
    
  def __createNote(self, note_length, pitch, volume):
    return Note(note_length, pitch, volume)

  def addNote(self, start_time, note):
    # write the note to the track
    if (start_time not in self.track.notes):
      self.track.notes[start_time] = list()
    self.track.notes[start_time].append(note)
      
    # save the note if we're recording
    if (self.record_phrase == True):
      self.recorded_phrase.addNote(start_time, note)
        
  def buildTrack(self):
    channel = 0
    track_number = 0

    # do we always want it to start on 0?
    note_start_time = 0

    # for tracking how many chords we're recording
    record_index = 0
    phrase_length = 0

    note_count = self.__getRandom(self.config.note_config.count_scope)
    self.__logDebug("GENERAL", "Will be adding " + str(note_count) + " notes")

    # generates tuple of categories that will match up reasonably well with 
    # the probabilities specified when defining the chooser in the config
    self.categories = self.config.note_config.chooser.random(note_count)
    
    self.__logDebug("GENERAL", str(len(self.categories)) + " categories created")
    
    use_tempo_change = self.config.tempo_scope[0] != self.config.tempo_scope[1]

    if use_tempo_change:
      self.track.tempos[note_start_time] = self.__getRandom(self.config.tempo_scope)
    else:
      self.track.tempos[note_start_time] = self.config.tempo_scope[0]
    
    self.__logDebug("TEMPO", "TRACK  NOTE_START_TIME  TEMPO")
    self.__logDebug("TEMPO", str(track_number) + "  " + str(note_start_time) + "  " + str(self.track.tempos[note_start_time]))

    self.__logDebug("PITCH", "category  pitch  note_start_time  note_length  volume")

    for i,category in enumerate(self.categories):
    
      ################
      # TEMPO CHANGE #
      ################
      if use_tempo_change:
        tempo_change_chance = self.__getRandom(self.config.tempo_change_chance_range)
        if tempo_change_chance % self.config.tempo_change_chance == 0:
          self.track.tempos[note_start_time] = self.__getRandom(self.config.tempo_scope)

          self.__logDebug("TEMPO", str(track_number) + "  " + str(note_start_time) + "  " + str(self.track.tempos[note_start_time]))
      

      self.__logDebug("PITCH", "currently on category " + str(i))
    
      volume = self.__getRandom(self.config.volume_scope)
      note_length = self.__getRandom(self.config.note_config.length_scope)
  
      pitch = self.__generatePitch(True)

      if (phrase_length == 0):
        self.record_phrase = self.config.phrase_record_chance.random()
        
      if self.record_phrase == True:
        if (phrase_length == 0):
          phrase_length = self.__getRandom(self.config.phrase_length_scope)
          phrase_index = 0
          self.recorded_phrase = Phrase()

        if phrase_index < phrase_length:
          phrase_index += 1
        else:
          phrase_index = 0
          phrase_length = 0
          self.phrases.append(self.recorded_phrase)
          self.record_phrase = False

      self.addNote(note_start_time, self.__createNote(note_length, pitch, volume))
      
      self.__logDebug("PITCH", str(category) + "  " + str(pitch) + "  " + str(note_start_time) + "  " + str(note_length) + "  " + str(volume))
      
      ######################
      # SIMULTANEOUS NOTES #
      ######################
      simultaneous_pitches = [pitch]
      for j in range(self.config.note_config.max_simultaneous):
        self.__logDebug("PITCH", "on " + str(j) + " of " + str(self.config.note_config.max_simultaneous))
        
        if self.config.note_config.simultaneous_chance.random() == True:

          self.__logDebug("PITCH", "generating simultaneous note")
        
          try_to_generate_simultaneous_note = True
          
          while try_to_generate_simultaneous_note == True:
            # getting a pitch for a simultaneous note doesn't need to be limited by the category
            pitch = self.__generatePitch(False)

            if pitch in simultaneous_pitches: 
              # we don't want to add notes already used to the list of simultaneous pitches
              self.__logDebug("PITCH", "SIM NOTE failure: " + str(pitch) + " already used: " + str(simultaneous_pitches))
              try_to_generate_simultaneous_note = False
              break
            elif (pitch in self.config.note_config.categories[category]):
              # we don't want to add notes that are unpairable with the first note
              self.__logDebug("PITCH", "SIM NOTE failure: pitch " + str(pitch) + " is in the current category " + str(self.config.note_config.categories[category]))
              try_to_generate_simultaneous_note = False
            #elif (simultaneous_pitches[0] in self.config.note_config.unpairable and pitch in self.config.unpairable_notes[simultaneous_pitches[0]]):
            #  # we don't want to add notes that are unpairable with the first note
            #  self.__logDebug("PITCH", "SIM NOTE failure: simultaneous_pitches[0] " + str(simultaneous_pitches[0]) + " unpairable with " + str(pitch))
            #  break
            else:
              try_to_generate_simultaneous_note = False
              note_length = self.__getRandom(self.config.note_config.length_scope)
              self.addNote(note_start_time, self.__createNote(note_length, pitch, volume))

              self.__logDebug("PITCH", "SIM NOTE: " + str(category) + " " + str(pitch) + " " + str(note_start_time) + " " + str(note_length) + " " + str(volume))

        else:
          self.__logDebug("PITCH", "NOT generating simultaneous note")
          break

      # determine next note_start_time AFTER adding the first note
      # so that we always start the track with the first note @ 0
      old_note_start_time = note_start_time

      try:
        start_time_factor = self.__getRandom(self.config.start_time_factors)
      except AttributeError:
        start_time_factor = 1

      # self.__getRandom(self.config.note_length_scope) or note_length in here?
      # maybe make this configurable?
      note_start_time = note_start_time + int(note_length / start_time_factor)

      if note_start_time < 0:
        note_start_time *= -1



        
  def writeTrack(self):
    print(self.track.__repr__)

  def importJsonFileToTrack(self, filename):
    with open(filename, 'r') as f:
      content = f.read()

    self.track = jsonpickle.decode(content)

  def exportTrackToJsonFile(self, customIdentifier):
    id = customIdentifier
    if id == "":
      id += "."
    
    filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".json"

    with open(filename, "w") as f:
      f.write(self.track.__repr__())
    
    return filename


  def convertTrackToMidi(self):
    track_number = 0
    channel = 0

    # add tempos
    for start_time in self.track.tempos:
      #print("start_time: " + str(start_time) + " tempo: " + str(self.track.tempos[start_time]))
      self.midi.addTempo(int(track_number), int(start_time), int(self.track.tempos[start_time]))

    # add notes
    for start_time in self.track.notes:
      #print("start_time: " + str(start_time))
      for note in self.track.notes[start_time]:
        self.midi.addNote(int(track_number), int(channel), int(note.pitch), int(start_time), int(note.length), int(note.volume))
        #print("  length: " + str(note.length) + " pitch: " + str(note.pitch) + " volume: " + str(note.volume))

  def exportMidiFile(self, customIdentifier):
    id = customIdentifier
    if id == "":
      id += "."

    filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".mid"
      
    with open(filename, "wb") as output_file:
      self.midi.writeFile(output_file)
      
    return filename

  def writeStats(self):
    self.__logDebug("GENERAL", self.config.getStats())
    self.__logDebug("GENERAL", lea.vals(*self.categories))

  def writeLog(self):
    debug_tables = self.debug_tables
    for table_name in debug_tables:
      logging.debug(table_name)
      for line in debug_tables[table_name]:
        logging.debug(line)
      logging.debug("")

##################
# STATIC METHODS #
##################
  @staticmethod
  def __getRandom(*args):
    if (len(args) == 1):
      if (isinstance(args[0], int)):
        return random.randrange(args[0])
      else:
        if (isinstance(args[0], list)):
          if (len(args[0]) == 2):
            if (args[0][0] == args[0][1]):
              return args[0][0]
            else:
              num = random.randrange(args[0][0], args[0][1])
              #print("returning " + str(num) + " which is between " + str(args[0][0]) + " and " + str(args[0][1]))
              return num
          else:
            return args[0][random.randrange(len(args[0]))]
        else:
          if ((isinstance(args[0], tuple))):
            rnd = random.randrange(len(args[0]))
            return args[0][rnd]
          else:
            raise TypeError("first arg must be a list or int. right now it's:" + str(type(args[0])))
    else:
      raise TypeError("first arg must be a list or int. right now it's not set to anything.")

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

