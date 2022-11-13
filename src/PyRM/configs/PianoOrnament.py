import PyRM.configs.NoteCategory
import PyRM.configs.ConfigVolume

class ConfigNote:
  def __init__(self):
    self.allow_simultaneous_from_same_category = False
    self.force_simultaneous_from_same_category = False

    # 21 (A0) to 108 (C8) is the range of an 88 key piano
    self.categories = {
      NoteCategory.LOW.value: list(range(20, 40)),
      NoteCategory.MIDDLE.value: list(range(41, 85)),
      NoteCategory.HIGH.value: list(range(85, 109))
    }
    
    self.count_scope = [10, 20]

    self.forbidden_notes = []
    
    self.format_names = tuple(("Low", "High", "BothEven", "BothLowFavored", "BothHighFavored"))
    
    self.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.LOW.value,)), 
                                    tuple((1,))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HIGH.value,)), 
                                    tuple((1,))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), 
                                    tuple((0.5,0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), 
                                    tuple((0.75,0.25))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), 
                                    tuple((0.25,0.75))
                                ))
                               ]
    
    self.format_probabilities = [lea.pmf(definition) for definition in self.format_definitions]

    self.formats = dict(zip(self.format_names, self.format_probabilities))
    
    self.format_change_chooser = lea.pmf({
      False: 0.5,
      True: 0.5
    })

    self.format_chooser = lea.pmf({
      "Low": 0.05,
      "High": 0.35,
      "BothEven": 0.3, 
      "BothLowFavored": 0.05,
      "BothHighFavored": 0.25
     })
    # from a quarter note to half note
    self.length_scope = [self.ticks_per_quarternote, self.ticks_per_quarternote*2]

    self.map = MapPianoOrnament()

    self.length_maps = self.map.length_maps
    self.length_map_chooser = self.map.length_map_chooser

    self.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
    for category in self.categories:
      self.categories[category] = list(set(self.categories[category]) - set(self.forbidden_notes))
      self.scope = self.scope + self.categories[category]

    self.simultaneous_chance = lea.pmf({
      False: 0.75,
      True: 0.25
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
    self.count_scope = [5, 10]
    self.record_chance = lea.pmf({
      False: 1,
      True: 0
    })
    self.replay_chance = lea.pmf({
      False: 1,
      True: 0
    })

class PianoOrnament():
  def __init__(self):
    self.name = "OrnamentPiano"
    self.debug_log = False

    self.note = NoteConfig()

    self.phrase = PhraseConfig()

    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
