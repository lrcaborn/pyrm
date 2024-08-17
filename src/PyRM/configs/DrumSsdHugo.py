import lea
from PyRM.configs.ConfigNoteBase import ConfigNoteBase
from PyRM.configs.ConfigVolume import ConfigVolume
from PyRM.configs.MapDrumSlow import MapDrumSlow
from PyRM.configs.NoteCategory import NoteCategory
from PyRM.configs.ClusterCategory import ClusterCategory
import jsonpickle

class ConfigNote(ConfigNoteBase):
  def __init__(self, ticks_per_quarternote):
    super().__init__(ticks_per_quarternote) 

    self.allow_simultaneous_from_same_category = True
    self.force_simultaneous_from_same_category = False
# unused
# MIDI note/CC name map
# 76 Clap
# 75 Cowbell
# 74 Cowbell Shank
# 79 Tambourine Hit
# 78 Tambourine Down
# 77 Tambourine Up
# 58 Ride Choke
# 56 Crash Right Choke
# 54 Crash Left Choke
# 49 Splash Choke
# 32 China Choke
# 39 Snare Rimclick
# 19 Rack Tom 1 Rimclick
# 17 Rack Tom 2 Rimclick
# 14 Floor Tom 1 Rimclick
# 12 Floor Tom 2 Rimclick
# 46 Hi-Hat Tip CC Controlable
# 26 Hi-Hat Shank CC Controllable


    self.categories = {
      NoteCategory.CRASH.value: [93,92,91,90,57,55,50,31],
      NoteCategory.HAT.value: [73,72,71,70,69,68,67,66,65,64,63,62,61,60,44,42,22],
      NoteCategory.KICK.value: [36,35],
      NoteCategory.RIDE.value: [59,53,52,51],
      NoteCategory.SNARE.value: [40,38,37,34,33,21],
      NoteCategory.TOM.value: [48,47,45,43,41]
    }

    self.count_scope = [100, 500]
	
    # formats are used when NOT using sequences.
    # formats define the note groupings that MAY be played together.
    # probabilities for how often the note classes are chosen are assigned
    self.format_names = tuple(("All", "CrashHatKickSnareTom", "CrashKickRideSnareTom", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "KickRideSnareTom", "RideSnare", "RideTom"))
	
    self.format_definitions = [
      dict(zip(
        tuple((NoteCategory.CRASH.value, NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.RIDE.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
        tuple((0.05, 0.15, 0.3, 0.15, 0.2, 0.15))
      )),
      dict(zip(
        tuple((NoteCategory.CRASH.value, NoteCategory.HAT.value, NoteCategory.KICK.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
        tuple((0.05, 0.15, 0.35, 0.25, 0.2))
      )),
      dict(zip(
        tuple((NoteCategory.CRASH.value, NoteCategory.KICK.value, NoteCategory.RIDE.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
        tuple((0.05, 0.35, 0.15, 0.25, 0.2))
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
        tuple((NoteCategory.KICK.value, NoteCategory.RIDE.value, NoteCategory.SNARE.value, NoteCategory.TOM.value)), 
        tuple((0.25, 0.25, 0.25, 0.25))
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
      "All": 0.05,
      "CrashHatKickSnareTom": 0.05,
      "CrashKickRideSnareTom": 0.05,
      "CrashSnare": 0.05,
      "CrashTom": 0.05, 
      "HatSnare": 0.15,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.1,
      "HatRide": 0.1,
      "KickRideSnareTom": 0.1,
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
      False: 0.65,
      True: 0.35
    })
    self.replay_chance = lea.pmf({
      False: 0.65,
      True: 0.35
    })

class DrumSsdHugo():
  def __init__(self, ticks_per_quarternote):
    self.name = "SsdHugo"
    self.debug_log = False

    self.note = ConfigNote(ticks_per_quarternote)
    
    self.phrase = ConfigPhrase()
    
    self.space = self.note.map.space
    self.space.chance = lea.pmf({
      False: 0.975,
      True: 0.025
    })
    # seconds
    self.space.scope = (0.25, 1.5)

    self.use_randomized_tuning = False

    self.volume = ConfigVolume()

  def json(self):
    return jsonpickle.encode(self)
    