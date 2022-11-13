import lea
from PyRM.configs.ConfigNote import ConfigNote
from PyRM.configs.ConfigVolume import ConfigVolume
from PyRM.configs.MapDrumSlow import MapDrumSlow
from PyRM.configs.NoteCategory import NoteCategory

class ConfigNote:
  def __init__(self, ticks_per_quarternote):
    self.allow_simultaneous_from_same_category = False
    self.force_simultaneous_from_same_category = False

    self.categories = {
      NoteCategory.CRASH.value: [27, 28, 29, 49, 54, 55, 83, 94, 95], 
      NoteCategory.HAT.value: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 61, 62, 63, 64, 65, 119, 120, 121, 122, 123, 124], 
      NoteCategory.KICK.value: [34], 
      NoteCategory.RIDE.value: [30, 31, 32, 51, 52, 53, 57, 58, 59, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118], 
      NoteCategory.SNARE.value: [6, 33, 38, 39, 40, 66, 67, 68, 69, 70, 71, 125, 126, 127],  
      NoteCategory.TOM.value: [4, 5, 41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
    }

    self.count_scope = [500, 750]
	
#    self.forbidden_notes = {1, 2, 3, 4, 5, 35, 36, 37, 56, 67, 71, 76} # 37 is the only sidestick in brush kit, add 127, 71, 67 if using the full ezx kits

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
      False: 0.5,
      True: 0.5
    })

    self.format_chooser = lea.pmf({
      "All": 0.15,
      "CrashSnare": 0.1,
      "CrashTom": 0.1, 
      "HatSnare": 0.1,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.15,
      "HatRide": 0.1,
      "RideSnare": 0.1,
      "RideTom": 0.1
     })
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.length_scope = [ticks_per_quarternote*16, ticks_per_quarternote*32]

    self.map = MapDrumSlow()

    self.length_maps = self.map.length_maps
    self.length_map_chooser = self.map.length_map_chooser

    self.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
 #   for category in self.categories:
 #     self.categories[category] = list(set(self.categories[category]) - self.forbidden_notes)
  #    self.scope = self.scope + self.categories[category]

    self.simultaneous_chance = lea.pmf({
      False: 0.35,
      True: 0.65
    })

    self.ticks_per_quarternote = 480 # can be up to 960

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [3, 15]
    self.record_chance = lea.pmf({
      False: 0.65,
      True: 0.35
    })
    self.replay_chance = lea.pmf({
      False: 0.65,
      True: 0.35
    })

class DrumEzxJazz():
  def __init__(self, ticks_per_quarternote):
    self.name = "EzxJazz"
    self.debug_log = False

    self.note = ConfigNote(ticks_per_quarternote)
    
    self.phrase = ConfigPhrase()
    
    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
