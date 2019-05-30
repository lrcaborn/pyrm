#!/usr/bin/env python
import jsonpickle
import lea
import logging
import random
import uuid

from midiutil import MIDIFile
from operator import attrgetter

def jsonDefault(OrderedDict):
    return OrderedDict.__dict__

#class Logger:
#    class __Logger:
#        def __init__(self):
#            self.debug_tables = {
#                "GENERAL": [],
#                "PITCH": [],
#                "RECORDING": [],
#                "TEMPO": [],
#                "TUNING": []
#            }
#
#        #def log_debug(self, debug_table, message):
#            #self.debug_tables[debug_table].append(message)
#
#    instance = None
#
#    def __init__(self):
#        if not Logger.instance:
#            Logger.instance = Logger.__Logger()
#
#    def __getattr__(self, name):
#        return getattr(self.instance, name)
#
#    def log_debug(self, debug_table, message):
#        __Logger.log_debug(debug_table, message)
#
#logger = Logger()
        
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
    def __init__(self, config, tempo_length_map):
        self.config = config

        # do we always want it to start on 0?
        self.note_start_time = 0

        # notes is key/value with key being start time and 
        # value being a list of note objects
        self.notes = dict()
        
        self.record_phrase = False
        # recorded_phrases is a list for now
        # I'm hoping to expand it to have a lea chooser so that
        # it will move toward having equal selection of the
        # different recorded phrases OR if possible, preference
        # for certain phrases. Perhaps longer ones.
        self.recorded_phrases = list()

        self.tempo_length_map = tempo_length_map

        # tempos is just key/value. 
        # Key = start time and value is the tempo
        self.tempos = dict()


    def import_json(self, filename):
        with open(filename, 'r') as f:
            content = f.read()

        self.track = jsonpickle.decode(content)

    def export_to_json_file(self, customIdentifier):
        id = customIdentifier
        if id == "":
            id += "."
        
        filename = self.config.name + "." + str(id) + str(uuid.uuid4()) + ".json"

        with open(filename, "w") as f:
            f.write(self.track.__repr__())
        
        return filename

    def add_note(self, note):
        # write the note to the track
        if (self.note_start_time not in self.notes):
            self.notes[self.note_start_time] = list()
        self.notes[self.note_start_time].append(note)
            
        # save the note if we're recording
        if (self.record_phrase == True):
            self.recorded_phrase.add_note(self.note_start_time, note)

    def _create_note(self, note_length, pitch, volume):
        return Note(note_length, pitch, volume)

    def _generate_pitch(self, isPrimaryNote):
        try:
            category = self.config.note.chooser.random()
            if isPrimaryNote:
                range = self.config.note.categories[category]
                pitch = get_random(range)
                #logger.log_debug("PITCH", 
                #                    "HAVE CHOOSER - PRIMARY pitch: " + str(pitch) + 
                #                    " from category: " + str(category) + 
                #                    " with range: " + str(range))
            else:
                range = self.config.note.scope
                pitch = get_random(range)
                #logger.log_debug("PITCH", 
                #                    "HAVE CHOOSER - NONPRIMARY pitch: " + str(pitch) + 
                #                    " from category: " + str(category) + 
                #                    " with range: " + str(range))
        except AttributeError:
            range = self.config.note.scope
            pitch = get_random(range)
            pitch = get_random(range)
            #logger.log_debug("PITCH", 
            #                    "NO CHOOSER - pitch: " + str(pitch) + 
            #                    " from range: " + str(range))

        return pitch

    def build_track(self):
        channel = 0
        track_number = 0

        # for tracking how many chords we're recording
        record_index = 0
        phrase_count = 0

        # generates tuple of categories that will match up reasonably well 
        # with the probabilities specified when defining the chooser in 
        # the config
        self.categories = self.config.note.chooser.random(self.note_count)
        
        #logger.log_debug("GENERAL", 
        #                        str(len(self.categories)) + " categories created")
        
        use_tempo_change = self.config.tempo.scope[0] != self.config.tempo.scope[1]

        if use_tempo_change:
            self.tempos[self.note_start_time] = get_random(self.config.tempo.scope)
            #print("initial tempo: " + str(self.tempos[note_start_time]))
        else:
            self.tempos[self.note_start_time] = self.config.tempo.scope[0]
        
        #logger.log_debug("TEMPO", "TRACK    NOTE_START_TIME    TEMPO")
        #logger.log_debug("TEMPO", 
        #                    str(track_number) + "    " + 
        #                    str(note_start_time) + "    " + 
        #                    str(self.tempos[note_start_time]))

        #logger.log_debug("PITCH", 
        #                    "category    pitch    note_start_time    note_length    volume")

        for i,category in enumerate(self.categories):
        
            ################
            # TEMPO CHANGE #
            ################
            if use_tempo_change:
                tempo_change_chooser = self.config.tempo.change_chooser.random()
                if tempo_change_chooser:
                    self.tempos[self.note_start_time] = get_random(self.config.tempo.scope)
                    #print("changing tempo to: " + str(self.tempos[note_start_time]) + " scope: " + str(self.config.tempo.scope))

                    #logger.log_debug("TEMPO", 
                    #                    str(track_number) + "    " + 
                    #                    str(note_start_time) + "    " + 
                    #                    str(track.tempos[note_start_time]))
            
            #logger.log_debug("PITCH", "currently on category " + str(i))
        
            volume = get_random(self.config.volume_scope)
            note_length = get_random(self.config.note.length_scope)
    
            pitch = self._generate_pitch(True)
            
            ###############
            #  RECORDING  #
            ###############
            # setup
            if (phrase_count == 0):
                self.record_phrase = self.config.phrase.record_chance.random()
                if (self.record_phrase):
                    self.recorded_phrase = Phrase()
                    phrase_index = 0
                    phrase_count = get_random(self.config.phrase.count_scope)
                    #logger.log_debug("RECORDING", "Initializing record_phrase, " 
                    #                + str(phrase_count) + " phrases to be recorded")

            self.add_note(self._create_note(note_length, pitch, volume))
            
            #logger.log_debug("PITCH", 
            #                    str(category) + "    " + 
            #                    str(pitch) + "    " + 
            #                    str(note_start_time) + "    " + 
            #                    str(note_length) + "    " + 
            #                    str(volume))
            
            ######################
            # SIMULTANEOUS NOTES #
            ######################
            simultaneous_pitches = [pitch]
            for j in range(self.config.note.max_simultaneous):
                #logger.log_debug("PITCH", "on " + str(j) + " of " 
                #                 + str(self.config.note.max_simultaneous))
                
                if self.config.note.simultaneous_chance.random() == True:
                    #logger.log_debug("PITCH", "generating simultaneous note")
                
                    try_to_generate_simultaneous_note = True
                    
                    # getting a pitch for a simultaneous note doesn't need to be limited by the category
                    pitch = self._generate_pitch(False)

                    if pitch in simultaneous_pitches: 
                        # we don't want to add notes already used to the list of simultaneous pitches
                        #logger.log_debug("PITCH", 
                        #                    "SIM NOTE failure: " + str(pitch) + 
                        #                    " already used: " 
                        #                    + str(simultaneous_pitches))
                        break
                    elif (pitch in self.config.note.categories[category]):
                        if (self.config.note.allow_simultaneous_from_same_category == False):
                            # we don't want to add notes that are unpairable with the first note
                            #logger.log_debug("PITCH", 
                            #                "SIM NOTE failure: pitch " + str(pitch) + 
                            #                " is in the current category " + 
                            #                str(self.config.note.categories[category]))
                            continue
                    else:
                        note_length = get_random(self.config.note.length_scope)
                        self.add_note(self._create_note(note_length, pitch, volume))

                        #logger.log_debug("PITCH", 
                        #                    "SIM NOTE: " + str(category) 
                        #                    + " " + str(pitch) 
                        #                    + " " + str(note_start_time) 
                        #                    + " " + str(note_length) 
                        #                    + " " + str(volume))

                else:
                    #logger.log_debug("PITCH", "NOT generating simultaneous note")
                    break

            # index management and storage of recorded phrases
            # add_note handles storing the notes in phrases
            if (self.record_phrase == True):
                if phrase_index < phrase_count:
                    phrase_index += 1
                else:
                    phrase_index = 0
                    phrase_count = 0
                    #logger.log_debug("RECORDING", 
                    #                "Adding notes from record_phrase and resetting")
                    self.recorded_phrases.append(self.recorded_phrase)
                    self.record_phrase = self.config.phrase.record_chance.random()
            else:
                self.record_phrase = self.config.phrase.record_chance.random()
                
            self.note_start_time = self.calculate_note_start_time()

            self.replay_phrase = self.config.phrase.replay_chance.random()
            if (self.replay_phrase and len(self.recorded_phrases) > 0):
                self.record_phrase = False # override recording so that we don't re-record recorded phrases.
                phrase = random.choice(self.recorded_phrases)

                for chord in phrase.chords.values():
                    note_length = chord[0].length
                    for note in chord:
                        self.add_note(note)
                    self.note_start_time = self.calculate_note_start_time()

    def calculate_note_start_time(self):
        # if we can't find the tempo for the current note_start_time,
        # go with the next earliest one that's stored.
        tempo = self.tempos[self.note_start_time] if self.note_start_time in self.tempos else self.tempos[min(self.tempos.keys(), key=lambda k: abs(k-self.note_start_time))]
        length_factors = [t[1] for t in self.tempo_length_map if t[0][0] <= tempo and t[0][1] >= tempo]
        start_time_factor = get_random(length_factors[0])
        if start_time_factor == 0:
            start_time_factor = 1

        # determine next note_start_time AFTER adding the first note to the track
        # so that we always start the track with the first note @ 0
        self.note_start_time = self.note_start_time + int(self.config.note.ticks_per_quarternote / start_time_factor)

        if self.note_start_time < 0:
            self.note_start_time *= -1

        if self.config.space.chance.random() == True:
            space_scope_factor = get_random(self.config.space.scope)
            # tempo = 180bpm
            # that's 180 / 60 beats per seconds
            # if we're using 480 ticks per quarter note, that's 
            # 480 * 3 = 1440 ticks
            # 1440 * rand # between 5 and 10 (let's say 7)
            # total tick count for this silence == 1440 * 7 == 10080
            ticks_of_silence = (tempo / 60.0) * self.config.ticks_per_quarternote * space_scope_factor
            self.note_start_time += ticks_of_silence
            
        return self.note_start_time

    def write_track(self):
        print(self.__repr__)


    #def __repr__(self):
    #    return jsonpickle.encode(self)
    #    #return json.dumps(self, default=jsonDefault, indent=4)

class PyRM:
    def __init__(self, config):
        #logging.basicConfig(filename='debug.log',level=logging.DEBUG)

        self.currentTrack = None
        self.tracks = []
        self.midis = []

        # tempo_length_map links a tempo tuple with a length factor tuple
        # if a note is added within a tempo tuple's range, the note length
        # will be adjusted by a factor between the high and low length factors
        self.tempo_length_map = self.build_tempo_length_map(1, 39, 1.5, 1.116, 9)

        #self._load_config(config)            
        #self.track = Track()
        #self.midi = MIDIFile(1, 
        #                deinterleave = False, 
        #                eventtime_is_ticks = True, 
        #                ticks_per_quarternote = config.ticks_per_quarternote)
        
        self.config = config        
        for track_config in self.config.track_configs:
            # ticks_per_quarternote and tempo info from the improv concifg
            # should always override whatever might be in the individual track.
            # eventually, both of those should be removed from track config.
            track_config.ticks_per_quarternote = self.config.ticks_per_quarternote
            track_config.tempo = self.config.tempo

            track = Track(track_config, self.tempo_length_map)
            track.note_count = get_random(track.config.note.count_scope)
            #logger.log_debug("GENERAL", "Will be adding " + str(track.note_count) + " notes")
            self.tracks.append(track)
        
            midi = MIDIFile(1, 
                            deinterleave = False, 
                            eventtime_is_ticks = True, 
                            ticks_per_quarternote = config.ticks_per_quarternote)
            self.midis.append(midi)

    def export_to_midi_files(self, customIdentifier):
        id = customIdentifier
        if id == "":
            id += "."

        for index, midi in enumerate(self.midis):
            filename = self.tracks[index].config.name + "." + str(id) + str(uuid.uuid4()) + ".mid"

            with open(filename, "wb") as output_file:
                midi.writeFile(output_file)
            
        return filename

    def convert_tracks_to_midi_objects(self):
        for index,track in enumerate(self.tracks):
            track_number = 0
            channel = 0

            # add tempos
            for start_time in track.tempos:
                #print("start_time: " + str(start_time) + " tempo: " + str(self.track.tempos[start_time]))
                self.midis[index].addTempo(int(track_number), int(start_time), int(track.tempos[start_time]))

            # add notes
            for start_time in track.notes:
                #print("start_time: " + str(start_time))
                for note in track.notes[start_time]:
                    self.midis[index].addNote(int(track_number), int(channel), int(note.pitch), int(start_time), int(note.length), int(note.volume))
                    #print("    length: " + str(note.length) + " pitch: " + str(note.pitch) + " volume: " + str(note.volume))
 
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
        #config_info = "using " + config.name + " configuration"

    def _frequency(self, midi_note):
        """Calculate frequency of given midi note"""
        return 27.5 * 2 ** ((midi_note - 21)/12)

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

            #for count, value in enumerate(base_tuning):
                #logger.log_debug("TUNING", value, " ", new_tuning[count])

            self.midi.changeNoteTuning(0, new_tuning, tuningProgam=0)

    def build_tracks(self):
        for track in self.tracks:
            track.build_track()
            print("tracks note_start_time: " + str(track.note_start_time))

        # find the longest track
        max_note_start_time = max(self.tracks, key=attrgetter('note_start_time')).note_start_time
        print("max_note_start_time: " + str(max_note_start_time))

        

    #def write_stats(self):
        #logger.log_debug("GENERAL", self.config.getStats())
        #logger.log_debug("GENERAL", lea.vals(*self.categories))

    def write_log(self):
        pass
        #for track in self.tracks:
        #    debug_tables = track.debug_tables
        #    for table_name in debug_tables:
        #        logging.debug(table_name)
        #        for line in debug_tables[table_name]:
        #            logging.debug(line)
        #        logging.debug("")

##################
# STATIC METHODS #
##################
def get_random(*args):
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

def greater_of(first, second):
    if first > second:
        return first
    else:
        return second

def lesser_of(first, second):
    if first < second:
        return first
    else:
        return second

