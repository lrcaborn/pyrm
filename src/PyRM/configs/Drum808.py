import PyRM.configs.ConfigVolume
import PyRM.configs.ConfigVolume

class ConfigNote:
  def __init__(self):
    self.allow_simultaneous_from_same_category = False
    self.force_simultaneous_from_same_category = False

    self.categories = {
      NoteCategory.CRASH.value: [49],
      NoteCategory.FX.value: [37, 39, 40, 44, 47, 48, 50, 51], # 37 snare rim, 39 clap, 40 clave, 44 maraca, 47, 48, 50 conga, 51 "cowbell"
      NoteCategory.HAT.value: [42, 46], 
      NoteCategory.KICK.value: [36], 
      NoteCategory.SNARE.value: [38],
      NoteCategory.TOM.value: [41, 43, 45]
    }

    self.count_scope = [25, 100]
	
    self.forbidden_notes = []

    self.format_names = tuple(("HatSnare", "KickSnare", "HatKickSnare", "CrashHatKickSnare", "CrashHatKickSnareTom"))

    self.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.SNARE.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.KICK.value, NoteCategory.SNARE.value)), 
                                    tuple((0.4, 0.6))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.SNARE.value)), 
                                    tuple((0.4, 0.3, 0.3))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.CRASH.value, NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.SNARE.value)), 
                                    tuple((0.075, 0.375, 0.275, 0.275))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.CRASH.value, NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
                                    tuple((0.075, 0.35, 0.25, 0.25, 0.075))
                                )),
                               ]
							   
    self.format_probabilities = [lea.pmf(definition) for definition in self.format_definitions]

    self.formats = dict(zip(self.format_names, self.format_probabilities))

    self.format_change_chooser = lea.pmf({
      False: 0.5,
      True: 0.5
    })

    self.format_chooser = lea.pmf({
      "HatSnare": 0.05,
      "KickSnare": 0.5,
      "HatKickSnare": 0.3,
      "CrashHatKickSnare": 0.1,
      "CrashHatKickSnareTom": 0.05
     })
	
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.length_scope = [self.ticks_per_quarternote*16, self.ticks_per_quarternote*32]

    self.map = MapDrumSlow()

    self.length_maps = self.map.length_maps
    self.length_map_chooser = self.map.length_map_chooser

    self.max_simultaneous = 0

    # remove forbidden notes from all categories and the full note scope
    for category in self.categories:
      self.categories[category] = list(set(self.categories[category]) - self.forbidden_notes)
      self.scope = self.scope + self.categories[category]

    self.simultaneous_chance = lea.pmf({
      False: 1,
      True: 0
    })
	
    self.ticks_per_quarternote = 480 # can be up to 960

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [7, 15]
    self.record_chance = lea.pmf({
      False: 0.8,
      True: 0.2
    })
    self.replay_chance = lea.pmf({
      False: 0.1,
      True: 0.9
    })

class Drum808():
  def __init__(self):
    self.name = "Drum808"
    self.debug_log = False

    self = ConfigNote()
    
    self.phrase = ConfigPhrase()
    
    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
