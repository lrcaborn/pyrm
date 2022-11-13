import PyRM.configs.NoteCategory
import PyRM.configs.ConfigVolume

class ConfigNote:
  def __init__(self):
    self.allow_simultaneous_from_same_category = False
    self.force_simultaneous_from_same_category = False

    self.categories = {
      NoteCategory.HAT.value: [21, 22, 23, 24, 25, 26, 42, 44, 60, 65], 
      NoteCategory.KICK.value: [34, 36], 
      NoteCategory.RIDE.value: [51, 53, 59, 84, 85, 86, 89, 90, 91, 96, 97, 98, 101, 102, 103], 
      NoteCategory.SNARE.value: [33, 38, 39, 40, 69, 70],  
      NoteCategory.CRASH.value: [27, 28, 29, 30, 31, 32, 49, 52, 54, 55, 57, 58, 93, 94, 95, 105, 106, 107, 117, 118], 
      NoteCategory.TOM.value: [41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
    }

    self.count_scope = [25, 100]

    self.forbidden_notes = {37, 71} # 37 and 71 is sidestick

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
      False: 0.25,
      True: 0.75
    })

    self.format_chooser = lea.pmf({
      "All": 0.15,
      "CrashSnare": 0.1,
      "CrashTom": 0.1, 
      "HatSnare": 0.125,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.1,
      "HatRide": 0.1,
      "SnareRide": 0.125,
      "RideTom": 0.1
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
      False: 0.25,
      True: 0.75
    })

    self.ticks_per_quarternote = 480 # can be up to 960

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [5, 25]
    self.record_chance = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.replay_chance = lea.pmf({
      False: 0.5,
      True: 0.5
    })

class DrumHell():
  def __init__(self):
    self.name = "EzxDKFH"
    self.debug_log = False

    self.note = ConfigNote()
    
    self.phrase = ConfigPhrase()
    
    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
