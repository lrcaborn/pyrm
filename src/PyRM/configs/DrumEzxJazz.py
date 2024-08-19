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

    self.categories = {
      NoteCategory.CRASH.value: [27, 28, 29, 49, 54, 55, 83, 94, 95], 
      NoteCategory.HAT.value: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 61, 62, 63, 64, 65, 119, 120, 121, 122, 123, 124], 
      NoteCategory.KICK.value: [34], 
      NoteCategory.RIDE.value: [30, 31, 32, 51, 52, 53, 57, 58, 59, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118], 
      NoteCategory.SNARE.value: [6, 33, 38, 39, 40, 66, 67, 68, 69, 70, 71, 125, 126, 127],  
      NoteCategory.TOM.value: [4, 5, 41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
    }

    self.count_scope = [100, 500]
	
    # segments are groupings of consecutive clusters
    self.segments = {
      "Verse": {
        ClusterCategory.CRASH: (1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.HAT:  (0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0),
        ClusterCategory.KICK:  (1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.RIDE:  (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.SNARE: (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.TOM:  (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
      },
      "Chorus": {
        ClusterCategory.CRASH: (1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.HAT:  (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.KICK:  (1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.RIDE:  (0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0),
        ClusterCategory.SNARE: (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0),
        ClusterCategory.TOM:  (0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
      },
    }

    # a sequence is a grouping of consecutive segments
    #self.sequence = (self.segments["VERSE"], self.segments["CHORUS"], self.segments["VERSE"], self.segments["CHORUS"], )

    # with 64 spots, every 1 is a 64th, 2 is 32nd, 4 is 16th, 8 is 8th, 16 is quarter, 32 is half
    # half to figure out triplets for swing
    #self.segment_definitions[ClusterCategory.HAT]
  
    # clusters are used only with sequences.
    # clusters define the note groupings that must be played together.
    self.cluster_definitions = {
      ClusterCategory.CRASH.value: tuple(NoteCategory.CRASH.value), 
      ClusterCategory.HAT.value: tuple(NoteCategory.HAT.value), 
      ClusterCategory.KICK.value: tuple(NoteCategory.KICK.value), 
      ClusterCategory.RIDE.value: tuple(NoteCategory.RIDE.value), 
      ClusterCategory.SNARE.value: tuple(NoteCategory.SNARE.value), 
      ClusterCategory.TOM.value: tuple(NoteCategory.TOM.value)
    }


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
      False: 0.55,
      True: 0.45
    })

class DrumEzxJazz():
  def __init__(self, ticks_per_quarternote):
    self.name = "EzxJazz"
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
    