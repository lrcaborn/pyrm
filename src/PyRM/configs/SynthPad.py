import lea
import random
from math import ceil
from PyRM.configs.ConfigNoteBase import ConfigNoteBase
from PyRM.configs.ConfigVolume import ConfigVolume
from PyRM.configs.MapSynthPad import MapSynthPad
from PyRM.configs.NoteCategory import NoteCategory

class ConfigNote(ConfigNoteBase):
    def __init__(self, ticks_per_quarternote):
        super().__init__(ticks_per_quarternote) 
    
        self.allow_simultaneous_from_same_category = True
        self.force_simultaneous_from_same_category = False
    
        lowest_note = 21
        lowest_starting_note = 54
        starting_note = random.randint(lowest_starting_note, lowest_starting_note+12)
        octave_count = round(8 - ((starting_note - lowest_note) / 12))
        print("lowest_starting_note: " + str(lowest_starting_note))
        print("starting_note: " + str(starting_note))
        print("octave_count: " + str(octave_count))
    
        # 21 (A0) to 108 (C8) is the range of an 88 key piano
        self.categories = {
          NoteCategory.LOW.value: list(range(20, 40)),
          NoteCategory.MIDDLE.value: list(range(41, 85)),
          NoteCategory.HIGH.value: list(range(85, 109)),

          NoteCategory.ACOUSTIC.value: super().generate_scale_notes(NoteCategory.ACOUSTIC, starting_note, octave_count),
          NoteCategory.AEOLIAN_DOMINANT.value: super().generate_scale_notes(NoteCategory.AEOLIAN_DOMINANT, starting_note, octave_count),
          NoteCategory.ALGERIAN.value: super().generate_scale_notes(NoteCategory.ALGERIAN, starting_note, octave_count),
          NoteCategory.ALGERIAN_2.value: super().generate_scale_notes(NoteCategory.ALGERIAN_2, starting_note, octave_count),
          NoteCategory.AUGMENTED.value: super().generate_scale_notes(NoteCategory.AUGMENTED, starting_note, octave_count),
          NoteCategory.BALINESE.value: super().generate_scale_notes(NoteCategory.BALINESE, starting_note, octave_count),
          NoteCategory.BYZANTINE.value: super().generate_scale_notes(NoteCategory.BYZANTINE, starting_note, octave_count),
          NoteCategory.CHINESE.value: super().generate_scale_notes(NoteCategory.CHINESE, starting_note, octave_count),
          NoteCategory.DIMINISHED.value: super().generate_scale_notes(NoteCategory.DIMINISHED, starting_note, octave_count),
          NoteCategory.DOMINANT_DIMINISHED.value: super().generate_scale_notes(NoteCategory.DOMINANT_DIMINISHED, starting_note, octave_count),
          NoteCategory.EGYPTIAN.value: super().generate_scale_notes(NoteCategory.EGYPTIAN, starting_note, octave_count),
          NoteCategory.EIGHT_TONE_SPANISH.value: super().generate_scale_notes(NoteCategory.EIGHT_TONE_SPANISH, starting_note, octave_count),
          NoteCategory.HARMONIC_MINOR.value: super().generate_scale_notes(NoteCategory.HARMONIC_MINOR, starting_note, octave_count),
          NoteCategory.HAWAIIAN.value: super().generate_scale_notes(NoteCategory.HAWAIIAN, starting_note, octave_count),
          NoteCategory.HIRAJŌSHI.value: super().generate_scale_notes(NoteCategory.HIRAJŌSHI, starting_note, octave_count),
          NoteCategory.HUNGARIAN.value: super().generate_scale_notes(NoteCategory.HUNGARIAN, starting_note  , octave_count),
          NoteCategory.HUNGARIAN_MAJOR.value: super().generate_scale_notes(NoteCategory.HUNGARIAN_MAJOR, starting_note, octave_count),
          NoteCategory.IBERIAN.value: super().generate_scale_notes(NoteCategory.IBERIAN, starting_note, octave_count),
          NoteCategory.IWATO.value: super().generate_scale_notes(NoteCategory.IWATO, starting_note, octave_count),
          NoteCategory.JAPANESE.value: super().generate_scale_notes(NoteCategory.JAPANESE, starting_note, octave_count),
          NoteCategory.NEOPOLITAN_MAJOR.value: super().generate_scale_notes(NoteCategory.NEOPOLITAN_MAJOR, starting_note, octave_count),
          NoteCategory.NEOPOLITAN_MINOR.value: super().generate_scale_notes(NoteCategory.NEOPOLITAN_MINOR, starting_note, octave_count),
          NoteCategory.ORIENTAL.value: super().generate_scale_notes(NoteCategory.ORIENTAL, starting_note, octave_count),
          NoteCategory.PHRYGIAN_DOMINANT.value: super().generate_scale_notes(NoteCategory.PHRYGIAN_DOMINANT, starting_note, octave_count),
          NoteCategory.PROMETHEUS.value: super().generate_scale_notes(NoteCategory.PROMETHEUS, starting_note, octave_count),
          NoteCategory.ROMANIAN_MINOR.value: super().generate_scale_notes(NoteCategory.ROMANIAN_MINOR, starting_note, octave_count),
          NoteCategory.SUPER_LOCRIAN.value: super().generate_scale_notes(NoteCategory.SUPER_LOCRIAN, starting_note, octave_count),
          NoteCategory.WHOLE_TONE.value: super().generate_scale_notes(NoteCategory.WHOLE_TONE, starting_note, octave_count),
          NoteCategory.YO.value: super().generate_scale_notes(NoteCategory.YO, starting_note, octave_count)

        }

        self.count_scope = [10, 20]

        self.forbidden_notes = []

        self.format_names = tuple(("Low", "Middle", "High", "LowMiddle_Even", "MiddleHigh_MiddleFavored", "All",                   "Acoustic","Algerian","Algerian2","Aeolian Dominant","Augmented","Balinese",
                  "Byzantine","Chinese","Chromatic","Diminished","Dominant Diminished","Egyptian",
                  "Eight Tone Spanish","Hawaiian","Harmonic Minor","Hirajōshi","Hungarian",
                  "Hungarian major","Iberian","Iwato","Japanese","Neopolitan Major","Neopolitan Minor",
                  "Oriental","Phrygian Dominant","Prometheus","Romanian Minor","Super Locrian",
                  "Whole Tone","Yo"))
        
        self.format_definitions = [
                                    dict(zip(tuple((NoteCategory.LOW.value,)), tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.MIDDLE.value,)), tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HIGH.value,)), tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.LOW.value, NoteCategory.MIDDLE.value)), tuple((0.5, 0.5)))),
                                    dict(zip(tuple((NoteCategory.MIDDLE.value, NoteCategory.HIGH.value)), tuple((0.7, 0.3)))),
                                    dict(zip(tuple((NoteCategory.LOW.value, NoteCategory.MIDDLE.value, NoteCategory.HIGH.value)), tuple((0.2, 0.6, 0.2)))),
                                    dict(zip(tuple((NoteCategory.ACOUSTIC.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.ALGERIAN.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.ALGERIAN_2.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.AEOLIAN_DOMINANT.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.AUGMENTED.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.BALINESE.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.BYZANTINE.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.CHINESE.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.CHROMATIC.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.DIMINISHED.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.DOMINANT_DIMINISHED.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.EGYPTIAN.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.EIGHT_TONE_SPANISH.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HAWAIIAN.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HARMONIC_MINOR.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HIRAJŌSHI.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HUNGARIAN.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HUNGARIAN_MAJOR.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.IBERIAN.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.IWATO.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.JAPANESE.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.NEOPOLITAN_MAJOR.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.NEOPOLITAN_MINOR.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.ORIENTAL.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.PHRYGIAN_DOMINANT.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.PROMETHEUS.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.ROMANIAN_MINOR.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.SUPER_LOCRIAN.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.WHOLE_TONE.value,)),tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.YO.value,)),tuple((1,))))
                                ]
        
        self.format_probabilities = [lea.pmf(definition) for definition in self.format_definitions]

        self.formats = dict(zip(self.format_names, self.format_probabilities))

        self.format_change_chooser = lea.pmf({
          False: 1,
          True: 0
        })

        self.format_chooser = lea.pmf({
          "Low": 0,
          "Middle": 0,
          "High": 0,
          "LowMiddle_Even": 0, 
          "MiddleHigh_MiddleFavored": 0,
          "All": 0,
          "Acoustic": 0,
          "Algerian": 0,
          "Algerian2": 0,
          "Aeolian Dominant": 0,
          "Augmented": 0,
          "Balinese": 0,
          "Byzantine": 0,
          "Chinese": 0,
          #"Chromatic": 0,
          "Diminished": 0,
          "Dominant Diminished": 0,
          "Egyptian": 1,
          "Eight Tone Spanish": 0,
          "Hawaiian": 0,
          "Harmonic Minor": 0,
          "Hirajōshi": 0,
          "Hungarian": 0,
          "Hungarian major": 0,
          "Iberian": 0,
          "Iwato": 0,
          "Japanese": 0,
          "Neopolitan Major": 0,
          "Neopolitan Minor": 0,
          "Oriental": 0,
          "Phrygian Dominant": 0,
          "Prometheus": 0,
          "Romanian Minor": 0,
          "Super Locrian": 0,
          "Whole Tone": 0,
          "Yo": 0
         })
        
        # from half a measure to 4 measures
        self.length_scope = [ticks_per_quarternote*16, ticks_per_quarternote*64]

        self.map = MapSynthPad()

        self.length_maps = self.map.length_maps
        self.length_map_chooser = self.map.length_map_chooser

        self.max_simultaneous = 2

        self.simultaneous_chance = lea.pmf({
          False: 0.9,
          True: 0.1
        })

        self.ticks_per_quarternote = 480 # can be up to 960

class ConfigPhrase:
    def __init__(self):
        self.count_scope = [3, 10]
        self.record_chance = lea.pmf({
          False: 0.5,
          True: 0.5
        })
        self.replay_chance = lea.pmf({
          False: 0.85,
          True: 0.15
        })

class SynthPad():
    def __init__(self, ticks_per_quarternote):
        self.name = "Synth Pad"
        self.debug_log = False

        self.note = ConfigNote(ticks_per_quarternote)

        self.phrase = ConfigPhrase()

        self.space = self.note.map.space

        self.use_randomized_tuning = False

        self.volume = ConfigVolume()
