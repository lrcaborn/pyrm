import PyRM.configs.NoteCategory
import PyRM.configs.ConfigVolume

class ConfigNote:
  def __init__(self):
    self.allow_simultaneous_from_same_category = True
    self.force_simultaneous_from_same_category = True
    
    # 21 (A0) to 108 (C8) is the range of an 88 key piano
    self.categories = {
      NoteCategory.LOW.value: list(range(20, 40)),
      NoteCategory.MIDDLE.value: list(range(41, 85)),
      NoteCategory.HIGH.value: list(range(85, 109))
    }

    self.count_scope = [5, 25]

    self.forbidden_notes = []

    self.format_names = tuple(("Low", "Middle", "High", "LowMiddle", "MiddleHigh", "All"))
    
    self.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.LOW.value,)), 
                                    tuple((1,))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.MIDDLE.value,)), 
                                    tuple((1,))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HIGH.value,)), 
                                    tuple((1,))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.LOW.value, NoteCategory.MIDDLE.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.MIDDLE.value, NoteCategory.HIGH.value)), 
                                    tuple((0.7, 0.3))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.LOW.value, NoteCategory.MIDDLE.value, NoteCategory.HIGH.value)), 
                                    tuple((0.3, 0.7))
                                ))
                               ]
    
    self.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.format_change_chooser = lea.pmf({
      False: 0.25,
      True: 0.75
    })

    self.format_chooser = lea.pmf({
      "Low": 0.05,
      "Middle": 0.4,
      "High": 0.05,
      "LowMiddle": 0.2, 
      "MiddleHigh": 0.2,
      "All": 0.1
     })
    
    # from a 32nd note to 2 measures
    self.length_scope = [self.note.ticks_per_quarternote/8, self.note.ticks_per_quarternote*8]

    self.map = MapPianoComp()

    self.length_maps = self.map.length_maps
    self.length_map_chooser = self.map.length_map_chooser

    self.max_simultaneous = 4

    # remove forbidden notes from all categories and the full note scope
    for category in self.categories:
      self.categories[category] = list(set(self.categories[category]) - set(self.forbidden_notes))
      self.scope = self.scope + self.categories[category]

    self.simultaneous_chance = lea.pmf({
      False: 0.5,
      True: 0.5
    })

    self.ticks_per_quarternote = 480 # can be up to 960

class ConfigNoteHarmonicMinor(ConfigNote):
  def __init__(self):
    self.categories = {
      NoteCategory.HARMONICMINOR.value: [40,41,44,45,47,48,50,52,53,56,57,59,60,62,64,65,68,69,71,72,74,76],
    }
    self.chooser = lea.pmf({
      NoteCategory.HARMONICMINOR.value: 1
    })

    self.format_names = tuple(("HARMONICMINOR"))

    self.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.HARMONICMINOR.value,)), 
                                    tuple((1,))
                                ))
                               ]

    self.format_chooser = lea.pmf({
      "HARMONICMINOR": 1,
     })

class ConfigNoteJapanese(ConfigNote):
  def __init__(self):
    self.categories = {
      NoteCategory.JAPANESE.value: [40,41,45,47,48, 52,53,57,59,60, 61,65,67,68,72, 73,77,79,80,84]
    }
    self.chooser = lea.pmf({
      NoteCategory.JAPANESE.value: 1
    })

    self.format_names = tuple(("JAPANESE"))

    self.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.JAPANESE.value,)), 
                                    tuple((1,))
                                ))
                               ]

    self.format_chooser = lea.pmf({
      "JAPANESE": 1,
     })

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [3, 6]
    self.record_chance = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.replay_chance = lea.pmf({
      False: 0.6,
      True: 0.4
    })

class PianoComp():
  def __init__(self):
    self.name = "Comp Piano"
    self.debug_log = False
  
    self.note = NoteConfig()

    self.phrase = PhraseConfig()

    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
