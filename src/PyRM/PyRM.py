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
        return ("length: " + str(self.length) + " pitch: " + str(self.pitch) 
                + " volume: " + str(self.volume) + "\n")
        
class Phrase:
    def __init__(self):
        self.chords = dict()

    def add_note(self, start_time, note):
        if (start_time not in self.chords):
                self.chords[start_time] = list()
        
        self.chords[start_time].append(note)
        
    def __repr__(self):
        return str(self.chords)

class Track:
    def __init__(self):
        # tempos is just key/value. 
        # Key = start time and value is the tempo
        self.tempos = dict()
        # notes is key/value with key being start time and 
        # value being a list of note objects
        self.notes = dict()
        
        # recorded_phrases is a list for now
        # I'm hoping to expand it to have a lea chooser so that
        # it will move toward having equal selection of the
        # different recorded phrases OR if possible, preference
        # for certain phrases. Perhaps longer ones.
        self.recorded_phrases = list()
        
    def __repr__(self):
        return jsonpickle.encode(self)
        #return json.dumps(self, default=jsonDefault, indent=4)

class PyRM:
    def __init__(self, config):
        logging.basicConfig(filename='debug.log',level=logging.DEBUG)
        self._load_config(config)
        self.midi = MIDIFile(1, 
                        deinterleave = False, 
                        eventtime_is_ticks = True, 
                        ticks_per_quarternote = config.note_config.ticks_per_quarternote)
        self.debug_tables = {
            "GENERAL": [],
            "PITCH": [],
            "RECORDING": [],
            "TEMPO": [],
            "TUNING": []
        }
        self.track = Track()
        # tempo_length_map links a tempo tuple with a length factor tuple
        # if a note is added within a tempo tuple's range, the note length
        # will be adjusted by a factor between the high and low length factors
        self.tempo_length_map = self.build_tempo_length_map(1, 39, 1.5, 1.116, 9)
 
    def build_tempo_length_map(self, tempo_start, tempo_step, factor_start, factor_factor, count):
        index = 1
        tempo_length_map = []

        tempos = [tempo_start, 
                  tempo_start + tempo_step]
        length_factors = [factor_start, 
                          factor_start * factor_factor]

        while index <= count:
            index += 1
            tempo_length_map.append([tempos, length_factors])

            tempos = [tempos[1] + 1, 
                      tempos[1] + tempo_step]
            length_factors = [length_factors[1], 
                              length_factors[1] * factor_factor]

        return tempo_length_map
            
    def _load_config(self, config):
        self.config = config
        config_info = "using " + config.name + " configuration"

    def _frequency(self, midi_note):
        """Calculate frequency of given midi note"""
        return 27.5 * 2 ** ((midi_note - 21)/12)

    def _generate_pitch(self, isPrimaryNote):
        try:
            category = self.config.note_config.chooser.random()
            if isPrimaryNote:
                range = self.config.note_config.categories[category]
                pitch = self._get_random(range)
                self._log_debug("PITCH", 
                                    "HAVE CHOOSER - PRIMARY pitch: " + str(pitch) + 
                                    " from category: " + str(category) + 
                                    " with range: " + str(range))
            else:
                range = self.config.note_config.scope
                pitch = self._get_random(range)
                self._log_debug("PITCH", 
                                    "HAVE CHOOSER - NONPRIMARY pitch: " + str(pitch) + 
                                    " from category: " + str(category) + 
                                    " with range: " + str(range))
        except AttributeError:
            range = self.config.note_config.scope
            pitch = self._get_random(range)
            self._log_debug("PITCH", 
                                "NO CHOOSER - pitch: " + str(pitch) + 
                                " from range: " + str(range))

        return pitch

    def _generate_randomized_tuning(self):
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
                self._log_debug("TUNING", value, " ", new_tuning[count])

            self.midi.changeNoteTuning(0, new_tuning, tuningProgam=0)

    def _log_debug(self, debug_table, message):
        self.debug_tables[debug_table].append(message)
        #logging.debug(message)
        #print(message)
        
    def _create_note(self, note_length, pitch, volume):
        return Note(note_length, pitch, volume)

    def add_note(self, start_time, note):
        # write the note to the track
        if (start_time not in self.track.notes):
            self.track.notes[start_time] = list()
        self.track.notes[start_time].append(note)
            
        # save the note if we're recording
        if (self.record_phrase == True):
            self.recorded_phrase.add_note(start_time, note)
                
    def build_track(self):
        channel = 0
        track_number = 0

        # do we always want it to start on 0?
        note_start_time = 0

        # for tracking how many chords we're recording
        record_index = 0
        phrase_count = 0

        note_count = self._get_random(self.config.note_config.count_scope)
        self._log_debug("GENERAL", 
                            "Will be adding " + str(note_count) + " notes")

        # generates tuple of categories that will match up reasonably well 
        # with the probabilities specified when defining the chooser in 
        # the config
        self.categories = self.config.note_config.chooser.random(note_count)
        
        self._log_debug("GENERAL", 
                            str(len(self.categories)) + " categories created")
        
        use_tempo_change = self.config.tempo_scope[0] != self.config.tempo_scope[1]

        if use_tempo_change:
            self.track.tempos[note_start_time] = self._get_random(self.config.tempo_scope)
        else:
            self.track.tempos[note_start_time] = self.config.tempo_scope[0]
        
        self._log_debug("TEMPO", "TRACK    NOTE_START_TIME    TEMPO")
        self._log_debug("TEMPO", 
                            str(track_number) + "    " + 
                            str(note_start_time) + "    " + 
                            str(self.track.tempos[note_start_time]))

        self._log_debug("PITCH", 
                            "category    pitch    note_start_time    note_length    volume")

        for i,category in enumerate(self.categories):
        
            ################
            # TEMPO CHANGE #
            ################
            if use_tempo_change:
                tempo_change_chance = self._get_random(self.config.tempo_change_chance_range)
                if tempo_change_chance % self.config.tempo_change_chance == 0:
                    self.track.tempos[note_start_time] = self._get_random(self.config.tempo_scope)

                    self._log_debug("TEMPO", 
                                        str(track_number) + "    " + 
                                        str(note_start_time) + "    " + 
                                        str(self.track.tempos[note_start_time]))
            
            self._log_debug("PITCH", "currently on category " + str(i))
        
            volume = self._get_random(self.config.volume_scope)
            note_length = self._get_random(self.config.note_config.length_scope)
    
            pitch = self._generate_pitch(True)
            
            ###############
            #  RECORDING  #
            ###############
            # setup
            if (phrase_count == 0):
                self.record_phrase = self.config.phrase_record_chance.random()
                if (self.record_phrase):
                    self.recorded_phrase = Phrase()
                    phrase_index = 0
                    phrase_count = self._get_random(self.config.phrase_count_scope)
                    self._log_debug("RECORDING", "Initializing record_phrase, " 
                                    + str(phrase_count) + " phrases to be recorded")

            self.add_note(note_start_time, self._create_note(note_length, pitch, volume))
            
            self._log_debug("PITCH", 
                                str(category) + "    " + 
                                str(pitch) + "    " + 
                                str(note_start_time) + "    " + 
                                str(note_length) + "    " + 
                                str(volume))
            
            ######################
            # SIMULTANEOUS NOTES #
            ######################
            simultaneous_pitches = [pitch]
            for j in range(self.config.note_config.max_simultaneous):
                self._log_debug("PITCH", "on " + str(j) + " of " 
                                 + str(self.config.note_config.max_simultaneous))
                
                if self.config.note_config.simultaneous_chance.random() == True:
                    self._log_debug("PITCH", "generating simultaneous note")
                
                    try_to_generate_simultaneous_note = True
                    
                    # getting a pitch for a simultaneous note doesn't need to be limited by the category
                    pitch = self._generate_pitch(False)

                    if pitch in simultaneous_pitches: 
                        # we don't want to add notes already used to the list of simultaneous pitches
                        self._log_debug("PITCH", 
                                            "SIM NOTE failure: " + str(pitch) + 
                                            " already used: " 
                                            + str(simultaneous_pitches))
                        break
                    elif (pitch in self.config.note_config.categories[category]):
                        if (self.config.note_config.allow_simultaneous_from_same_category == False):
                            # we don't want to add notes that are unpairable with the first note
                            self._log_debug("PITCH", 
                                            "SIM NOTE failure: pitch " + str(pitch) + 
                                            " is in the current category " + 
                                            str(self.config.note_config.categories[category]))
                    else:
                        note_length = self._get_random(self.config.note_config.length_scope)
                        self.add_note(note_start_time, self._create_note(note_length, pitch, volume))

                        self. _log_debug("PITCH", 
                                            "SIM NOTE: " + str(category) 
                                            + " " + str(pitch) 
                                            + " " + str(note_start_time) 
                                            + " " + str(note_length) 
                                            + " " + str(volume))

                else:
                    self._log_debug("PITCH", "NOT generating simultaneous note")
                    break


            # index management and storage of recorded phrases
            # add_note handles storing the notes in phrases
            if (self.record_phrase == True):
                if phrase_index < phrase_count:
                    phrase_index += 1
                else:
                    phrase_index = 0
                    phrase_count = 0
                    self._log_debug("RECORDING", 
                                    "Adding notes from record_phrase and resetting")
                    self.track.recorded_phrases.append(self.recorded_phrase)
                    self.record_phrase = self.config.phrase_record_chance.random()
            else:
                self.record_phrase = self.config.phrase_record_chance.random()
                
            note_start_time = self.calculate_note_start_time(note_start_time)

            self.replay_phrase = self.config.phrase_replay_chance.random()
            if (self.replay_phrase and len(self.track.recorded_phrases) > 0):
                self.record_phrase = False # override recording so that we don't re-record recorded phrases.
                phrase = random.choice(self.track.recorded_phrases)

                for chord in phrase.chords.values():
                    note_length = chord[0].length
                    for note in chord:
                        self.add_note(note_start_time, note)
                    note_start_time = self.calculate_note_start_time(note_start_time)

    def calculate_note_start_time(self, note_start_time):
        # if we can't find the tempo for the current note_start_time,
        # go with the next earliest one that's stored.
        tempo = self.track.tempos[note_start_time] if note_start_time in self.track.tempos else self.track.tempos[min(self.track.tempos.keys(), key=lambda k: abs(k-note_start_time))]
        length_factors = [t[1] for t in self.tempo_length_map if t[0][0] <= tempo and t[0][1] >= tempo]
        start_time_factor = self._get_random(length_factors[0])
        if start_time_factor == 0:
            start_time_factor = 1

        # determine next note_start_time AFTER adding the first note to the track
        # so that we always start the track with the first note @ 0
        note_start_time = note_start_time 
                          + int(self.config.note_config.ticks_per_quarternote / start_time_factor)

        if note_start_time < 0:
            note_start_time *= -1
            
        return note_start_time

    def write_track(self):
        print(self.track.__repr__)

    def import_json_file_to_track(self, filename):
        with open(filename, 'r') as f:
            content = f.read()

        self.track = jsonpickle.decode(content)

    def export_track_to_json_file(self, customIdentifier):
        id = customIdentifier
        if id == "":
            id += "."
        
        filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".json"

        with open(filename, "w") as f:
            f.write(self.track.__repr__())
        
        return filename

    def convert_track_to_midi(self):
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
                self.midi.addNote(
                                int(track_number), int(channel), int(note.pitch), int(start_time), int(note.length), int(note.volume))
                #print("    length: " + str(note.length) + " pitch: " + str(note.pitch) + " volume: " + str(note.volume))

    def export_midi_file(self, customIdentifier):
        id = customIdentifier
        if id == "":
            id += "."

        filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".mid"
            
        with open(filename, "wb") as output_file:
            self.midi.writeFile(output_file)
            
        return filename

    def write_stats(self):
        self._log_debug("GENERAL", self.config.getStats())
        self._log_debug("GENERAL", lea.vals(*self.categories))

    def write_log(self):
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
    def _get_random(*args):
        if (len(args) == 1):
            if (isinstance(args[0], int)):
                return random.randrange(args[0])
            else:
                if (isinstance(args[0], list)):
                    if (len(args[0]) == 2):
                        if (args[0][0] == args[0][1]):
                            return args[0][0]
                        else:
                            #only call randrange if we're dealing with ints
                            if (isinstance(args[0][0], int) and isinstance(args[0][1], int)):
                                num = random.randrange(args[0][0], args[0][1])
                            else:
                                num = random.uniform(args[0][0], args[0][1])
                            return num
                    else:
                        return args[0][random.randrange(len(args[0]))]
                else:
                    if ((isinstance(args[0], tuple))):
                        return args[0][random.randrange(len(args[0]))]
                    else:
                        raise TypeError("first arg must be a list, tuple, or int. right now it's:" + str(type(args[0])))
        else:
            raise TypeError("first arg must be a list or int. right now it's not set to anything.")

    @staticmethod
    def _greater_of(first, second):
        if first > second:
            return first
        else:
            return second

    @staticmethod
    def _lesser_of(first, second):
        if first < second:
            return first
        else:
            return second

