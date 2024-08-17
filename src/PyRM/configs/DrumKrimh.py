import lea
from PyRM.configs.ConfigNoteBase import ConfigNoteBase
from PyRM.configs.ConfigVolume import ConfigVolume
from PyRM.configs.MapDrumSlow import MapDrumSlow
from PyRM.configs.NoteCategory import NoteCategory
from PyRM.configs.ClusterCategory import ClusterCategory

class ConfigNote(ConfigNoteBase):
  def __init__(self, ticks_per_quarternote):
    super().__init__(ticks_per_quarternote) 

    self.allow_simultaneous_from_same_category = True
    self.force_simultaneous_from_same_category = False

    self.categories = {
      NoteCategory.CRASH.value: [52, 54, 56, 58, 65, 67, 73, 75], 
      NoteCategory.HAT.value: [42, 41, 43, 44, 45, 46, 47, 48, 49, 50], 
      NoteCategory.KICK.value: [22, 23, 24], 
      NoteCategory.RIDE.value: [62, 63], # 61 is ride bell and it's quite loud
      NoteCategory.SNARE.value: [26, 27],  
      NoteCategory.TOM.value: [33, 34, 35, 36, 37]
    }

    self.count_scope = [250, 1000]
	
    # formats define the note groupings that MAY be played together.
    # probabilities for how often the note classes are chosen are assigned
    self.format_names = tuple(("All", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "KickRideSnareTom", "RideSnare", "RideTom"))
	
    self.format_definitions = [
      dict(zip(
        tuple((NoteCategory.CRASH.value, NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.RIDE.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
        tuple((0.05, 0.15, 0.25, 0.15, 0.25, 0.15))
      )),
      dict(zip(
        tuple((NoteCategory.CRASH.value, NoteCategory.SNARE.value)), 
        tuple((0.4, 0.6))
      )),
      dict(zip(
        tuple((NoteCategory.CRASH.value, NoteCategory.TOM.value)), 
        tuple((0.4, 0.6))
      )),
      dict(zip(
        tuple((NoteCategory.HAT.value, NoteCategory.SNARE.value)), 
        tuple((0.35, 0.65))
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
        tuple((NoteCategory.KICK.value, NoteCategory.RIDE.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
        tuple((0.3, 0.15, 0.25, 0.3))
      )),
      dict(zip(
        tuple((NoteCategory.RIDE.value, NoteCategory.SNARE.value)), 
        tuple((0.35, 0.65))
      )),
      dict(zip(
        tuple((NoteCategory.RIDE.value, NoteCategory.TOM.value)), 
        tuple((0.35, 0.65))
      ))
    ]

    self.format_probabilities = [lea.pmf(definition) for definition in self.format_definitions]

    self.formats = dict(zip(self.format_names, self.format_probabilities))

    self.format_change_chooser = lea.pmf({
      False: 0.5,
      True: 0.5
    })

    self.format_chooser = lea.pmf({
      "All": 0.05,
      "CrashSnare": 0.05,
      "CrashTom": 0.05, 
      "HatSnare": 0.15,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.15,
      "HatRide": 0.1,
      "KickRideSnareTom": 0.15,
      "RideSnare": 0.1,
      "RideTom": 0.1
     })
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.length_scope = [ticks_per_quarternote*16, ticks_per_quarternote*32]

    self.map = MapDrumSlow()

    self.length_maps = self.map.length_maps
    self.length_map_chooser = self.map.length_map_chooser

    self.max_simultaneous = 2

    self.simultaneous_chance = lea.pmf({
      False: 0.5,
      True: 0.5
    })

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [5, 15]
    self.record_chance = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.replay_chance = lea.pmf({
      False: 0.5,
      True: 0.5
    })

class DrumKrimh():
  def __init__(self, ticks_per_quarternote):
    self.name = "Krimh"
    self.debug_log = False

    self.note = ConfigNote(ticks_per_quarternote)
    
    self.phrase = ConfigPhrase()
    
    self.space = self.note.map.space

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()
