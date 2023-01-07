import lea
from PyRM.configs.ConfigNoteBase import ConfigNoteBase
from PyRM.configs.ConfigVolume import ConfigVolume
from PyRM.configs.MapPianoOrnament import MapPianoOrnament
from PyRM.configs.NoteCategory import NoteCategory


class ConfigNote(ConfigNoteBase):
    def __init__(self, ticks_per_quarternote):
        super().__init__(ticks_per_quarternote) 

        self.allow_simultaneous_from_same_category = False
        self.force_simultaneous_from_same_category = False

        # 21 (A0) to 108 (C8) is the range of an 88 key piano
        self.categories = {
            NoteCategory.LOW.value: super().generate_scale_notes(NoteCategory.CHROMATIC, 20, 2),
            NoteCategory.MIDDLE.value: super().generate_scale_notes(NoteCategory.CHROMATIC, 44, 4),
            NoteCategory.HIGH.value: super().generate_scale_notes(NoteCategory.CHROMATIC, 92, 2),
            NoteCategory.ACOUSTIC.value: super().generate_scale_notes(NoteCategory.ACOUSTIC, 40, 4),
            NoteCategory.AEOLIAN_DOMINANT.value: super().generate_scale_notes(NoteCategory.AEOLIAN_DOMINANT, 40, 4),
            NoteCategory.ALGERIAN.value: super().generate_scale_notes(NoteCategory.ALGERIAN, 40, 4),
            NoteCategory.ALGERIAN_2.value: super().generate_scale_notes(NoteCategory.ALGERIAN_2, 40, 4),
            NoteCategory.AUGMENTED.value: super().generate_scale_notes(NoteCategory.AUGMENTED, 40, 4),
            NoteCategory.BALINESE.value: super().generate_scale_notes(NoteCategory.BALINESE, 40, 4),
            NoteCategory.BYZANTINE.value: super().generate_scale_notes(NoteCategory.BYZANTINE, 40, 4),
            NoteCategory.CHINESE.value: super().generate_scale_notes(NoteCategory.CHINESE, 40, 4),
            NoteCategory.DIMINISHED.value: super().generate_scale_notes(NoteCategory.DIMINISHED, 40, 4),
            NoteCategory.DOMINANT_DIMINISHED.value: super().generate_scale_notes(NoteCategory.DOMINANT_DIMINISHED, 52, 2),
            NoteCategory.EGYPTIAN.value: super().generate_scale_notes(NoteCategory.EGYPTIAN, 40, 4),
            NoteCategory.EIGHT_TONE_SPANISH.value: super().generate_scale_notes(NoteCategory.EIGHT_TONE_SPANISH, 40, 4),
            NoteCategory.HARMONIC_MINOR.value: super().generate_scale_notes(NoteCategory.HARMONIC_MINOR, 30, 4),
            NoteCategory.HAWAIIAN.value: super().generate_scale_notes(NoteCategory.HAWAIIAN, 40, 4),
            NoteCategory.HIRAJŌSHI.value: super().generate_scale_notes(NoteCategory.HIRAJŌSHI, 40, 4),
            NoteCategory.HUNGARIAN.value: super().generate_scale_notes(NoteCategory.HUNGARIAN, 40, 4),
            NoteCategory.HUNGARIAN_MAJOR.value: super().generate_scale_notes(NoteCategory.HUNGARIAN_MAJOR, 40, 4),
            NoteCategory.IBERIAN.value: super().generate_scale_notes(NoteCategory.IBERIAN, 52, 4),
            NoteCategory.IWATO.value: super().generate_scale_notes(NoteCategory.IWATO, 52, 4),
            NoteCategory.JAPANESE.value: super().generate_scale_notes(NoteCategory.JAPANESE, 52, 4),
            NoteCategory.NEOPOLITAN_MAJOR.value: super().generate_scale_notes(NoteCategory.NEOPOLITAN_MAJOR, 52, 4),
            NoteCategory.NEOPOLITAN_MINOR.value: super().generate_scale_notes(NoteCategory.NEOPOLITAN_MINOR, 52, 4),
            NoteCategory.ORIENTAL.value: super().generate_scale_notes(NoteCategory.ORIENTAL, 52, 4),
            NoteCategory.PHRYGIAN_DOMINANT.value: super().generate_scale_notes(NoteCategory.PHRYGIAN_DOMINANT, 52, 4),
            NoteCategory.PROMETHEUS.value: super().generate_scale_notes(NoteCategory.PROMETHEUS, 52, 4),
            NoteCategory.ROMANIAN_MINOR.value: super().generate_scale_notes(NoteCategory.ROMANIAN_MINOR, 52, 4),
            NoteCategory.SUPER_LOCRIAN.value: super().generate_scale_notes(NoteCategory.SUPER_LOCRIAN, 52, 4),
            NoteCategory.WHOLE_TONE.value: super().generate_scale_notes(NoteCategory.WHOLE_TONE, 52, 4),
            NoteCategory.YO.value: super().generate_scale_notes(NoteCategory.YO, 52, 4)
        }
                
        self.count_scope = [10, 30]

        self.forbidden_notes = []
        
        self.format_names = tuple(("Low", "Middle", "High", "LowHigh_Even", "LowHigh_LowFavored", "LowHigh_HighFavored",
                                    "Acoustic","Algerian","Algerian2","Aeolian Dominant","Augmented","Balinese",
                                    "Byzantine","Chinese","Chromatic","Diminished","Dominant Diminished","Egyptian",
                                    "Eight Tone Spanish","Hawaiian","Harmonic Minor","Hirajōshi","Hungarian",
                                    "Hungarian major","Iberian","Iwato","Japanese","Neopolitan Major","Neopolitan Minor",
                                    "Oriental","Phrygian Dominant","Prometheus","Romanian Minor","Super Locrian",
                                    "Whole Tone","Yo"))
        
        self.format_definitions = [
                                    dict(zip(tuple((NoteCategory.LOW.value,)), tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.MIDDLE.value,)), tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HIGH.value,)), tuple((1,)))),
                                    dict(zip(tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), tuple((0.5,0.5)))),
                                    dict(zip(tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), tuple((0.75,0.25)))),
                                    dict(zip(tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), tuple((0.25,0.75)))),
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
            False: 0.5,
            True: 0.5
        })

        self.format_chooser = lea.pmf({
            "Low": 0,
            "Middle": 0,
            "High": 0,
            "LowHigh_Even": 0, 
            "LowHigh_LowFavored": 0,
            "LowHigh_HighFavored": 0,
            "Acoustic": 0,
            "Algerian": 0,
            "Algerian2": 0,
            "Aeolian Dominant": 0,
            "Augmented": 0.5,
            "Balinese": 0,
            "Byzantine": 0,
            "Chinese": 0,
            "Chromatic": 0,
            "Diminished": 0,
            "Dominant Diminished": 0,
            "Egyptian": 0,
            "Eight Tone Spanish": 0,
            "Hawaiian": 0,
            "Harmonic Minor": 0,
            "Hirajōshi": 0.2,
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
            "Super Locrian": 0.5,
            "Whole Tone": 0,
            "Yo": 0
         })
         
        # from a quarter note to half note
        self.length_scope = [ticks_per_quarternote, ticks_per_quarternote*2]

        self.map = MapPianoOrnament()

        self.length_maps = self.map.length_maps
        self.length_map_chooser = self.map.length_map_chooser

        self.max_simultaneous = 2

        self.simultaneous_chance = lea.pmf({
            False: 0.75,
            True: 0.25
        })	


class ConfigPhrase:
    def __init__(self):
        self.count_scope = [5, 10]
        self.record_chance = lea.pmf({
            False: 0.75,
            True: 0.25
        })
        self.replay_chance = lea.pmf({
            False: 0.75,
            True: 0.25
        })

class PianoOrnament():
    def __init__(self, ticks_per_quarternote):
        self.name = "OrnamentPiano"
        self.debug_log = False

        self.note = ConfigNote(ticks_per_quarternote)

        self.phrase = ConfigPhrase()

        self.space = self.note.map.space

        self.use_randomized_tuning = False

        self.volume = ConfigVolume()
