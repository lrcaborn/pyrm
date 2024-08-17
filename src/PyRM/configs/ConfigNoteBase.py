import lea
from PyRM.configs.NoteCategory import NoteCategory

class ConfigNoteBase:
    def __init__(self, ticks_per_quarternote):
        self.allow_simultaneous_from_same_category = False
        self.categories = {}
        self.chooser = None
        self.count_scope = []
        self.forbidden_notes = {}
        self.force_simultaneous_from_same_category = False
        self.length_maps = {}
        self.length_map_chooser = None
        self.length_scope = []
        self.map = None
        self.max_simultaneous = 0
        self.scale_definitions = {
                NoteCategory.ACOUSTIC: (2,2,2,1,2,1,2),
                NoteCategory.AEOLIAN_DOMINANT: (2,2,1,2,1,2,2),
                NoteCategory.ALGERIAN: (2,1,3,1,1,3,2),
                NoteCategory.ALGERIAN_2: (2,1,2,1,1,1,3,1),
                NoteCategory.AUGMENTED: (3,1,3,1,3,1),
                NoteCategory.BALINESE: (1,2,4,1,4),
                NoteCategory.BYZANTINE: (1,3,1,2,1,3,1),
                NoteCategory.CHINESE: (4,2,1,4,1),
                NoteCategory.CHROMATIC: (1,1,1,1,1,1,1,1,1,1,1,1),
                NoteCategory.DIMINISHED: (2,1,2,1,2,1,2,1 ),
                NoteCategory.DOMINANT_DIMINISHED: (1,2,1,2,1,2,1,2),
                NoteCategory.EGYPTIAN: (2,3,2,3,2),
                NoteCategory.EIGHT_TONE_SPANISH: (1,2,1,1,1,2,2,2),
                NoteCategory.HARMONIC_MINOR: (2,1,2,2,1,3,1),
                NoteCategory.HAWAIIAN: (2,1,2,2,2,2,1,),
                NoteCategory.HIRAJŌSHI: (2,1,4,1,4),
                NoteCategory.HUNGARIAN: (2,1,3,1,1,3,1),
                NoteCategory.HUNGARIAN_MAJOR: (3,1,2,1,2,1,2),
                NoteCategory.IBERIAN: (1,3,1,2,3,2),
                NoteCategory.IWATO: (1,4,1,4,2),
                NoteCategory.JAPANESE: (1,4,2,3,2),
                NoteCategory.NEOPOLITAN_MAJOR: (1,2,2,2,2,2,1),
                NoteCategory.NEOPOLITAN_MINOR: (1,2,2,2,1,3,1),
                NoteCategory.ORIENTAL: (1,3,1,1,3,1,2),
                NoteCategory.PHRYGIAN_DOMINANT: (2,1,3,1,2,1,2),
                NoteCategory.PROMETHEUS: (2,2,2,3,1,2),
                NoteCategory.ROMANIAN_MINOR: (2,1,3,1,2,1,2),
                NoteCategory.SUPER_LOCRIAN: (1,2,1,2,2,2,2),
                NoteCategory.WHOLE_TONE: (2,2,2,2,2,2),
                NoteCategory.YO: (2,3,2,2,3)
        }
        self.scope = []
        self.simultaneous_chance = lea.pmf({
            True: 1,
            False: 0
        })
        self.span_scope = []
        self.ticks_per_quarternote = ticks_per_quarternote

    def generate_scale_notes(self, noteCategory, start, count):
        steps = self.scale_definitions[noteCategory]
        note = start
        scale = (note,)
        for i in range(count):
            for step in steps:
                note += step
                scale += (note,)
        return scale
