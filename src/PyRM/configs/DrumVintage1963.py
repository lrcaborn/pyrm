import lea
from PyRM.configs.ConfigNoteBase import ConfigNoteBase
from PyRM.configs.ConfigVolume import ConfigVolume
from PyRM.configs.MapDrumSlow import MapDrumSlow
from PyRM.configs.NoteCategory import NoteCategory

class ConfigNote(ConfigNoteBase):
  def __init__(self, ticks_per_quarternote):
    super().__init__(ticks_per_quarternote) 

    self.allow_simultaneous_from_same_category = False
    self.force_simultaneous_from_same_category = False
    
    self.categories = {
      NoteCategory.HAT.value: [42, 44, 45, 46, 52, 54, 55, 58, 59, 60, 61, 62, 63, 64], 
      NoteCategory.KICK.value: [36],  # 36 is felt beater, 41 is plastic
      NoteCategory.RIDE.value: [50, 51, 53], 
      NoteCategory.SNARE.value: [38, 39, 40], # 38 snare, 39 snare edge, 40 rimshot
      NoteCategory.CRASH.value: [48, 49, 56, 57], 
      NoteCategory.TOM.value: [43, 47]
    }
    
    self.count_scope = [400, 600]

    self.forbidden_notes = {37} # 37 is sidestick

    self.format_names = tuple(("All", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "RideSnare", "RideTom"))
    
    self.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.CRASH.value, NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.RIDE.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
                                    tuple((0.05, 0.15, 0.3, 0.15, 0.2, 0.15))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.CRASH.value, NoteCategory.SNARE.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.CRASH.value, NoteCategory.TOM.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.SNARE.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.TOM.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
                                    tuple((0.25, 0.25, 0.25, 0.25))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.RIDE.value)), 
                                    tuple((0.5, 0.5))
                                )),
                                dict(zip(
                                    tuple((NoteCategory.RIDE.value, NoteCategory.SNARE.value)), 
                                    tuple((0.5, 0.5))
                                )),
                               dict(zip(
                                    tuple((NoteCategory.RIDE.value, NoteCategory.TOM.value)), 
                                    tuple((0.5, 0.5))
                                ))
                               ]
    
    self.format_probabilities = [lea.pmf(definition) for definition in self.format_definitions]

    self.formats = dict(zip(self.format_names, self.format_probabilities))

    self.format_change_chooser = lea.pmf({
      False: 0.75,
      True: 0.25
    })

    self.format_chooser = lea.pmf({
      "All": 0.2,
      "CrashSnare": 0,
      "CrashTom": 0, 
      "HatSnare": 0.2,
      "HatTom": 0.15,
      "HatKickSnareTom": 0.25,
      "HatRide": 0.05,
      "RideSnare": 0.1,
      "RideTom": 0.05
     })
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.length_scope = [self.ticks_per_quarternote*16, self.ticks_per_quarternote*32]

    self.map = MapDrumSlow()

    self.length_maps = self.map.length_maps
    self.length_map_chooser = self.map.length_map_chooser

    self.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
    for category in self.categories:
      self.categories[category] = list(set(self.categories[category]) - self.forbidden_notes)
      self.scope = self.scope + self.categories[category]

    self.simultaneous_chance = lea.pmf({
      False: 0.65,
      True: 0.35
    })
    
    self.ticks_per_quarternote = 480 # can be up to 960

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [5, 10]
    self.record_chance = lea.pmf({
      False: 0.25,
      True: 0.75
    })
    self.replay_chance = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    
class DrumVintage1963():
  def __init__(self, ticks_per_quarternote):
    self.name = "Vintage1963"
    self.debug_log = False

    self.note = ConfigNote(ticks_per_quarternote)
    
    self.phrase = ConfigPhrase()

    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
