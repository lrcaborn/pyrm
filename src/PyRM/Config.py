from enum import Enum
import numpy
import lea


class ImprovConfig:
  def __init__(self):
    self.track_configs = []
    # for now we will set it here and overwrite whatever is in the 
    # individual config.note.ticks_per_quarternote var
    self.ticks_per_quarternote = 480

    self.tempo = TempoConfig()
    self.tempo.scope_change_chooser = lea.pmf({
      False: 0.9,
      True: 0.1
    })
    self.tempo.change_chooser = lea.pmf({
      False: 0.1,
      True: 0.9
    })
    self.tempo.scope_chooser = lea.pmf(
    {
      0: 0,
      1: 0.2,
      2: 0.3,
      3: 0.5,
      4: 0
    })
    self.tempo.scopes = (
      (50, 100),
      (100, 150),
      (150, 200),
      (200, 250),
      (250, 300)
    )

    #self.tempo.scope_chooser = lea.pmf(
    #{
    #  0: 1
    #})
    #self.tempo.scopes = [
    #  (50, 110)
    #]

class MapPianoOrnament():
  def __init__(self):
    self.name = "Ornament Piano"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 9, (0.0625, 0.25)),
      "Name1": build_tempo_length_map((1, 301), 9, (0.0625, 0.5)),
      "Name2": build_tempo_length_map((1, 301), 9, (0.0625, 1.5)),
      "Name3": build_tempo_length_map((1, 301), 9, (0.125, 0.25)),
      "Name4": build_tempo_length_map((1, 301), 9, (0.125, 0.5)),
      "Name5": build_tempo_length_map((1, 301), 9, (0.125, 1.5))
     }
    self.length_map_chooser = lea.pmf({
      "Name0": 0.25,
      "Name1": 0.25,
      "Name2" : 0.25,
      "Name3": 0.15,
      "Name4": 0.05,
      "Name5": 0.05
    })

    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0.25,
      False: 0.75
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.25, 2)

class MapPianoComp():
  def __init__(self):
    self.name = "Piano Comp"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 20, (0.25, 1.5)),
      "Name1": build_tempo_length_map((1, 301), 5, (1, 2))
     }
    self.length_map_chooser = lea.pmf({
      "Name0": 0.6,
      "Name1": 0.4
    })

    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0.25,
      False: 0.75
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.25, 1.5)
    
class MapDrumSlow():
  def __init__(self):
    self.name = "Drum Slow"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 10, (0.9, 1.1)),
      "Name1": build_tempo_length_map((1, 301), 9, (0.25, 0.5)),
      "Name2": build_tempo_length_map((1, 301), 5, (0.5, 0.75)),
      "Name3": build_tempo_length_map((1, 301), 10, (0.0625, 0.25))
     }
     
    self.length_map_chooser = lea.pmf({
      "Name0": 0.4,
      "Name1": 0.1,
      "Name2": 0.5,
    })
    #self.length_map_chooser = lea.pmf({
    #  "Name0": 0.5,
    #  "Name1": 0.2,
    #  "Name2": 0.3,
    #  "Name3": 0
    #})
    
    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0.15,
      False: 0.85
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.1, 2)

class MapDrumFast():
  def __init__(self):
    self.name = "Drum Fast"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 9, (0.0625, 0.25)),
      "Name1": build_tempo_length_map((1, 301), 5, (0.0625, 0.125))
     }
     
    self.length_map_chooser = lea.pmf({
      "Name0": 0.4,
      "Name1": 0.6,
    })
    
    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0.25,
      False: 0.75
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.05, 0.250)

class NoteCategory(Enum):
  # drums
  COWBELL = "Cowbell"
  CRASH = "Cymbal Crashes"
  HAT = "Hi-Hat"
  KICK = "Kick"
  RIDE = "Ride cymbal"
  SNARE = "Snare"
  TOM = "Toms"
  FX = "FX"

  # piano sections
  LOW = "Low"
  MIDDLE = "Middle"
  HIGH = "High"
  
  # keys
  FMAJOR = "FMAJOR"
  
  def __str__(self):
    return self.name

#def calculate_modifier_end(modifier_start, modifier_adjustment):
#  return modifier_start * modifier_adjustment
#  #return modifier_start + (0.5 / modifier_adjustment)

# modifier 
# 1 = quarter note
# 0.25 = 16th note
# 8 = 2 measures	
def build_tempo_length_map(tempo_range, tempo_increment, modifier_range):
  tempo_length_map = []
  tempo_max = tempo_range[1]
  
  if tempo_max % tempo_increment != 0:
    tempo_max = tempo_range[1] + tempo_increment
  
  count = (tempo_max - tempo_range[0]) / tempo_increment
  modifier_increment = (modifier_range[1] - modifier_range[0]) / count
  
  tempos = numpy.arange(tempo_range[0], tempo_max, tempo_increment)
  modifiers = numpy.arange(modifier_range[0], modifier_range[1] + 0.0001, modifier_increment)
  
  index = 0
  
  while index < count - 1:
    tempo = (tempos[index], tempos[index + 1])
    modifier = (modifiers[0], modifiers[index + 1])
    tempo_length_map.append((tempo, modifier))
    index += 1

  return tempo_length_map

class NoteConfig:
  def __init__(self):
    self.categories = {}
    self.chooser = None
    self.count_scope = []
    self.forbidden_notes = {}
    self.length_maps = {}
    self.length_map_chooser = None
    self.length_scope = []
    self.max_simultaneous = 0
    self.scope = []
    self.simultaneous_chance = lea.pmf({
      True: 1,
      False: 0
    })
    self.span_scope = []
    self.ticks_per_quarternote = 480

class PhraseConfig:
  def __init__(self):
    self.count_scope = [5, 10]
    self.record_chance = lea.pmf({
      True: 0,
      False: 1
    })
    self.replay_chance = lea.pmf({
      True: 0,
      False: 1
    })

class SpaceConfig:
  def __init__(self):
    self.chance = lea.pmf({
      True: 0,
      False: 1
    })
    self.scope = (0,)

class TempoConfig:
  def __init__(self):
    self.scope_change_chooser = lea.pmf({
      False: 0.5,
      True: 0.5
    })
    self.change_chooser = lea.pmf({
      False: 1,
      True: 0
    })
    self.scope_chooser = lea.pmf(
    {
      0: 0,
      1: 0.25,
      2: 0.5,
      3: 0.25,
      4: 0
    })
    self.scopes = (
      (50, 100),
      (100, 150),
      (150, 200),
      (200, 250),
      (250, 300)
    )

class VolumeConfig:
  def __init__(self):
    self.scope_change_chooser = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.change_chooser = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.scope_chooser = lea.pmf(
    {
      0: 0.1,
      1: 0.3,
      2: 0.6,
      3: 0,
      4: 0,
      5: 0
    })
    self.scopes = (
      (0, 32),
      (32, 64),
      (64, 85),
      (86, 96),
      (97, 105),
      (106, 127)
    )


# 16 Bully Hats Open4
# 17-20
# 21 Bully Hats Pedal Closed
# 22 Bully Hats Closed Edge
# 23 Bully Hats Pedal Open
# 24 Bully Hats Open1
# 25 Bully Hats Open2
# 26 Bully Hats Open3
# 27 Bully Crash Cymbal1
# 28 Bully China Cymbal1
# 29 Bully Crash Cymbal3
# 30 Bully Spock Cymbal
# 31 Bully Crash Cymbal4
# 32 Bully Crash Cymbal6
# 32-34
# 36 Bully Kick Drum
# 37 Bully Snare Sidestick
# 38 Bully Snare Center Hits
# 39 Bully Snare Center Hits
# 40 Bully Snare Rimshots
# 41 Bully Floor Tom2
# 42 Bully Hats Closed Tip
# 43 Bully Floor Tom1
# 44 Bully Hats Pedal Closed
# 45 Bully Rack Tom2
# 46 Bully Hats Open2
# 47 Bully Rack Tom2
# 48 Bully Rack Tom1
# 49 Bully Crash Cymbal2
# 50 Bully Rack Tom1-D
# 51 Bully Ride Cymbal Tip
# 52 Bully China Cymbal2
# 53 Bully Ride Cymbal Bell
# 54 Bully Cowbell Tip
# 55 Bully Splash Cymbal
# 56 Bully Cowbell Edge
# 57 Bully Crash Cymbal5
# 58 
# 59 Bully Ride Cymbal Crash
# 60 Bully Hats Open5
# 61 
# 62 Bully Hats Tight Edge
# 63 Bully Hats Tight Tip
# 64 Bully Hats Open 0
# 65 Bully Hats Sequenced Hits
  
class DrumBully():
  def __init__(self):
    self.name = "BullyDrum"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False
    self.note.categories = {
      NoteCategory.HAT.value: [16, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 62, 63, 64, 65], 
      NoteCategory.CRASH.value: [27, 28, 29, 30, 31, 32, 49, 52, 55, 57, 59], 
      NoteCategory.KICK.value: [36], 
      NoteCategory.SNARE.value: [37, 38, 39, 40], 
      NoteCategory.TOM.value: [41, 43, 45, 47, 48, 50], 
      NoteCategory.RIDE.value: [51, 53], 
      NoteCategory.COWBELL.value: [54, 56]
    }
    self.note.chooser = lea.pmf({
      NoteCategory.COWBELL.value: 0,
      NoteCategory.CRASH.value: 0,
      NoteCategory.HAT.value: 0.15,
      NoteCategory.KICK.value: 0.30,
      NoteCategory.RIDE.value: 0.15,
      NoteCategory.SNARE.value: 0.25,
      NoteCategory.TOM.value: 0.10
    })
    self.note.count_scope = [1000, 1500]
    self.note.forbidden_notes = {17, 18, 19, 20, 33, 34, 35, 58, 61}
    self.note.length_scope = [self.note.ticks_per_quarternote*16, 
                     self.note.ticks_per_quarternote*32]
			
    #map = MapDrumFast()
    map = MapDrumSlow()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 3
	
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - self.note.forbidden_notes)
    self.note.scope = list(set(range(1, 128)) - self.note.forbidden_notes)

    self.note.simultaneous_chance = lea.pmf({
      True: 0.5,
      False: 0.5
    })

    self.note.ticks_per_quarternote = 480 # can be up to 960
    
    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 10]
    self.phrase.record_chance = lea.pmf({
      True: 0.2,
      False: 0.8
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.6,
      False: 0.4
    })

    self.space = map.space
    
    self.use_randomized_tuning = False
    self.volume = VolumeConfig()

class Drum808():
  def __init__(self):
    self.name = "Drum808"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False
    # 37 snare rim
    # 39 clap
    # 40 clave
    # 44 maraca
    # 47, 48, 50 conga
    # 51 "cowbell"
    self.note.categories = {
      NoteCategory.CRASH.value: [49],
      NoteCategory.FX.value: [37, 39, 40, 44, 47, 48, 50, 51],
      NoteCategory.HAT.value: [42, 46], 
      NoteCategory.KICK.value: [36], 
      NoteCategory.SNARE.value: [38],
      NoteCategory.TOM.value: [41, 43, 45]
    }
	
    self.note.format_names = tuple(("HatSnare", "HatKickSnare", "CrashHatKickSnare", "CrashHatKickSnareTom"))

    self.note.format_definitions = [
                                dict(zip(
                                    tuple((NoteCategory.HAT.value, NoteCategory.SNARE.value)), 
                                    tuple((0.5, 0.5))
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
							   
    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.note.format_change_chooser = lea.pmf({
      False: 0.9,
      True: 0.1
    })

    self.note.format_chooser = lea.pmf({
      "HatSnare": 0.05,
      "HatKickSnare": 0.8,
      "CrashHatKickSnare": 0.1,
      "CrashHatKickSnareTom": 0.05
     })
							   							   
    self.note.count_scope = [50, 100]

    self.note.forbidden_notes = set()
	
    self.note.length_scope = [self.note.ticks_per_quarternote*16, 
                     self.note.ticks_per_quarternote*32]

    #map = MapDrumFast()
    map = MapDrumSlow()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 0

    # remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - self.note.forbidden_notes)
      self.note.scope = self.note.scope + self.note.categories[category]
      #print(category + ": " + str(self.note.categories[category]))

    self.note.simultaneous_chance = lea.pmf({
      True: 0,
      False: 1
    })
	
    self.note.ticks_per_quarternote = 480 # can be up to 960
    
    self.phrase = PhraseConfig()
    self.phrase.count_scope = [7, 15]
    self.phrase.record_chance = lea.pmf({
      True: 0.2,
      False: 0.8
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.2,
      False: 0.8
    })
    
    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

class blahConfig():
  def __init__(self):
    self.pattern = {
      NoteCategory.CRASH.value: (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      NoteCategory.HAT.value: (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      NoteCategory.KICK.value: (1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0),
      NoteCategory.RIDE.value: (0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1),
      NoteCategory.SNARE.value: (0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0),
      NoteCategory.TOM.value: (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    }

class DrumBlues():
  def __init__(self):
    self.name = "EzxBlues"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False

    self.note.categories = {
      NoteCategory.HAT.value: [21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 61, 62, 63, 64, 65, ], 
      NoteCategory.KICK.value: [36], 
      NoteCategory.RIDE.value: [51, 52, 53, 54, 59], 
      NoteCategory.SNARE.value: [38, 39, 40],  
      NoteCategory.CRASH.value: [49, 50, 57, 58], 
      NoteCategory.TOM.value: [43, 48]
    }

    self.note.count_scope = [50, 150]
	
    self.note.format_names = tuple(("All", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "SnareRide"))
	
    self.note.format_definitions = [
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
                                ))
                               ]

    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.note.format_change_chooser = lea.pmf({
      False: 0.25,
      True: 0.75
    })

    self.note.format_chooser = lea.pmf({
      "All": 0.25,
      "CrashSnare": 0.1,
      "CrashTom": 0.1, 
      "HatSnare": 0.1,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.15,
      "HatRide": 0.1,
      "SnareRide": 0.1
     })

    # 37 is sidestick
    self.note.forbidden_notes = {37} 
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.note.length_scope = [self.note.ticks_per_quarternote*16, 
                     self.note.ticks_per_quarternote*32]

    map = MapDrumSlow()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - self.note.forbidden_notes)
      self.note.scope = self.note.scope + self.note.categories[category]

    self.note.simultaneous_chance = lea.pmf({
      True: 0.4,
      False: 0.6
    })

    self.note.ticks_per_quarternote = 480 # can be up to 960
    
    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 6]
    self.phrase.record_chance = lea.pmf({
      True: 0.3,
      False: 0.7
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.75,
      False: 0.25
    })
    
    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

class DrumEzxJazz():
  def __init__(self):
    self.name = "EzxJazz"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False

    self.note.categories = {
      NoteCategory.HAT.value: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 61, 62, 63, 64, 65, 119, 120, 121, 122, 123, 124], 
      NoteCategory.KICK.value: [34], 
      NoteCategory.RIDE.value: [30, 31, 32, 51, 52, 53, 57, 58, 59, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118], 
      NoteCategory.SNARE.value: [6, 33, 38, 39, 40, 66, 67, 68, 69, 70, 71, 125, 126, 127],  
      NoteCategory.CRASH.value: [27, 28, 29, 49, 54, 55, 83, 94, 95], 
      NoteCategory.TOM.value: [4, 5, 41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
    }

    self.note.count_scope = [500, 750]
	
    self.note.format_names = tuple(("All", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "RideSnare", "RideTom"))
	
    self.note.format_definitions = [
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

    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.note.format_change_chooser = lea.pmf({
      False: 0.5,
      True: 0.5
    })

    self.note.format_chooser = lea.pmf({
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

    # 37 is the only sidestick in brush kit
    # add 127, 71, 67 for full kits
    self.note.forbidden_notes = {1, 2, 3, 4, 5, 35, 36, 37, 56, 67, 71, 76} 
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.note.length_scope = [self.note.ticks_per_quarternote*16, 
                     self.note.ticks_per_quarternote*32]

    map = MapDrumSlow()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - self.note.forbidden_notes)
      self.note.scope = self.note.scope + self.note.categories[category]

    self.note.simultaneous_chance = lea.pmf({
      True: 0.65,
      False: 0.35
    })

    self.note.ticks_per_quarternote = 480 # can be up to 960
    
    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 15]
    self.phrase.record_chance = lea.pmf({
      True: 0.35,
      False: 0.65
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.35,
      False: 0.65
    })
    
    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

class DrumHell():
  def __init__(self):
    self.name = "EzxDKFH"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False

    self.note.categories = {
      NoteCategory.HAT.value: [21, 22, 23, 24, 25, 26, 42, 44, 60, 65], 
      NoteCategory.KICK.value: [34, 36], 
      NoteCategory.RIDE.value: [51, 53, 59, 84, 85, 86, 89, 90, 91, 96, 97, 98, 101, 102, 103], 
      NoteCategory.SNARE.value: [33, 38, 39, 40, 69, 70],  
      NoteCategory.CRASH.value: [27, 28, 29, 30, 31, 32, 49, 52, 54, 55, 57, 58, 93, 94, 95, 105, 106, 107, 117, 118], 
      NoteCategory.TOM.value: [41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
    }

    self.note.count_scope = [50, 150]
	
    self.note.format_names = tuple(("All", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "SnareRide"))
	
    self.note.format_definitions = [
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
                                ))
                               ]

    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.note.format_change_chooser = lea.pmf({
      False: 0.25,
      True: 0.75
    })

    self.note.format_chooser = lea.pmf({
      "All": 0.25,
      "CrashSnare": 0.1,
      "CrashTom": 0.1, 
      "HatSnare": 0.1,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.15,
      "HatRide": 0.1,
      "SnareRide": 0.1
     })

    # 37 and 71 is sidestick
    self.note.forbidden_notes = {37, 71} 
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.note.length_scope = [self.note.ticks_per_quarternote*16, 
                     self.note.ticks_per_quarternote*32]

    map = MapDrumSlow()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - self.note.forbidden_notes)
      self.note.scope = self.note.scope + self.note.categories[category]

    self.note.simultaneous_chance = lea.pmf({
      True: 0.75,
      False: 0.25
    })

    self.note.ticks_per_quarternote = 480 # can be up to 960
    
    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 10]
    self.phrase.record_chance = lea.pmf({
      True: 0.25,
      False: 0.75
    })
    self.phrase.replay_chance = lea.pmf({
      True: .9,
      False: 0.1
    })
    
    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

    
class DrumVintage1963():
  def __init__(self):
    self.name = "Vintage1963"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False
    self.note.categories = {
      NoteCategory.HAT.value: [42, 44, 45, 46, 52, 54, 55, 58, 59, 60, 61, 62, 63, 64], 
      # 36 is felt beater, 41 is plastic
      NoteCategory.KICK.value: [36], 
      NoteCategory.RIDE.value: [50, 51, 53], 
      # 38 snare
      # 39 snare edge
      # 40 rimshot
      NoteCategory.SNARE.value: [38, 39, 40],  
      NoteCategory.CRASH.value: [48, 49, 56, 57], 
      NoteCategory.TOM.value: [43, 47]
    }
    
    self.note.count_scope = [600, 800]

    self.note.format_names = tuple(("All", "CrashSnare", "CrashTom", "HatSnare", "HatTom", "HatKickSnareTom", "HatRide", "SnareRide"))
    
    self.note.format_definitions = [
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
                                ))
                               ]
    
    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.note.format_change_chooser = lea.pmf({
      False: 0.75,
      True: 0.25
    })

    self.note.format_chooser = lea.pmf({
      "All": 0.25,
      "CrashSnare": 0,
      "CrashTom": 0, 
      "HatSnare": 0.1,
      "HatTom": 0.1,
      "HatKickSnareTom": 0.2,
      "HatRide": 0.15,
      "SnareRide": 0.2
     })


    # 37 is sidestick
    self.note.forbidden_notes = {37} 
    
    # this is only really useful for making sure that cymbals left ringing don't cut out prematurely
    self.note.length_scope = [self.note.ticks_per_quarternote*16, 
                     self.note.ticks_per_quarternote*32]

    #map = MapDrumFast()
    map = MapDrumSlow()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 2

    # remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - self.note.forbidden_notes)
      self.note.scope = self.note.scope + self.note.categories[category]
      #print(category + ": " + str(self.note.categories[category]))

    #self.note.scope = list(set(range(1, 128)) - self.note.forbidden_notes)
    #print("full scope: " + str(self.note.scope))
    
    self.note.simultaneous_chance = lea.pmf({
      True: 0.35,
      False: 0.65
    })
    #self.simultaneous_note_category_behavior = SimultaneousNoteCategoryBehavior.DIFFERENT
    self.note.ticks_per_quarternote = 480 # can be up to 960
    
    self.phrase = PhraseConfig()
    self.phrase.count_scope = [5, 10]
    self.phrase.record_chance = lea.pmf({
      True: 0.35,
      False: 0.65
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.35,
      False: 0.65
    })
    
    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

class OrnamentPiano():
  def __init__(self):
    self.name = "OrnamentPiano"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = False
    self.note.force_simultaneous_from_same_category = False

    self.note.categories = {
      #NoteCategory.LOW.value: list(range(21, 56)),
      #NoteCategory.HIGH.value: list(range(57, 109))
      #NoteCategory.FMAJOR.value: [41,43,45,46,48,50,52,53,55,57,58,60,62,64] #f2
      NoteCategory.FMAJOR.value: [40,41,44,45,47,48,50,52,53,56,57,59,60,62,64,65,68,69,71,72,74,76]
    #  #NoteCategory.DMINOR.value: [38, 40, 41, 43, 45, 46, 48]
    }
    
    self.note.chooser = lea.pmf({
      #NoteCategory.LOW.value: 0.25,
      #NoteCategory.HIGH.value: 0.75,
      NoteCategory.FMAJOR.value: 1
    })
    self.note.count_scope = [50, 150]


    #self.note.format_names = tuple(("Low", "High", "BothEven", "BothLowFavored", "BothHighFavored"))
    self.note.format_names = tuple(("FMAJOR",))
    
    self.note.format_definitions = [
#                                dict(zip(
#                                    tuple((NoteCategory.LOW.value,)), 
#                                    tuple((1,))
#                                )),
#                                dict(zip(
#                                    tuple((NoteCategory.HIGH.value,)), 
#                                    tuple((1,))
#                                )),
#                                dict(zip(
#                                    tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), 
#                                    tuple((0.5,0.5))
#                                )),
#                                dict(zip(
#                                    tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), 
#                                    tuple((0.75,0.25))
#                                )),
#                                dict(zip(
#                                    tuple((NoteCategory.HIGH.value, NoteCategory.LOW.value)), 
#                                    tuple((0.25,0.75))
#                                ))
                                dict(zip(
                                    tuple((NoteCategory.FMAJOR.value,)), 
                                    tuple((1,))
                                ))
                               ]
    
    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]
    #print("format_probabilities: " + str(self.note.format_probabilities))

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))
    #print("formats: " + str(self.note.formats))
    
    self.note.format_change_chooser = lea.pmf({
      False: 1,
      True: 0
    })

    self.note.format_chooser = lea.pmf({
      #"Low": 0.1,
      #"High": 0.25,
      #"BothEven": 0.3, 
      #"BothLowFavored": 0.1,
      #"BothHighFavored": 0.25
      "FMAJOR": 1
     })
    
    self.note.forbidden_notes = []
    
    self.note.length_scope = [self.note.ticks_per_quarternote*8, 
                      self.note.ticks_per_quarternote*16]

    map = MapPianoOrnament()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 3

    # remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - set(self.note.forbidden_notes))
      self.note.scope = self.note.scope + self.note.categories[category]


    self.note.simultaneous_chance = lea.pmf({
      True: 0.35,
      False: 0.65
    })
	
    self.note.ticks_per_quarternote = 480 # can be up to 960

    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 10]
    self.phrase.record_chance = lea.pmf({
      True: 0.5,
      False: 0.5
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.5,
      False: 0.5
    })

    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

class CompPiano():
  def __init__(self):
    self.name = "Comp Piano"
    self.debug_log = False
  
    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = True
    self.note.force_simultaneous_from_same_category = True
    self.note.scope = [21, 109]
    self.note.categories = {
      NoteCategory.LOW.value: list(range(self.note.scope[0], 40)),
      NoteCategory.MIDDLE.value: list(range(41, 85)),
      NoteCategory.HIGH.value: list(range(85, self.note.scope[1]))
    }
    self.note.chooser = lea.pmf({
      NoteCategory.LOW.value: 0.05,
      NoteCategory.MIDDLE.value: 0.9,
      NoteCategory.HIGH.value: 0.05,
    })
    self.note.count_scope = [300, 400]

    self.note.format_names = tuple(("Low", "Middle", "High", "LowMiddle", "MiddleHigh", "All"))
    
    self.note.format_definitions = [
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
    
    self.note.format_probabilities = [lea.pmf(definition) for definition in self.note.format_definitions]

    self.note.formats = dict(zip(self.note.format_names, self.note.format_probabilities))

    self.note.format_change_chooser = lea.pmf({
      False: 0.25,
      True: 0.75
    })

    self.note.format_chooser = lea.pmf({
      "Low": 0.05,
      "Middle": 0.4,
      "High": 0.05,
      "LowMiddle": 0.2, 
      "MiddleHigh": 0.2,
      "All": 0.1
     })
    
    self.note.forbidden_notes = []


    # from a 32nd note to 2 measures
    self.note.length_scope = [self.note.ticks_per_quarternote/8, 
                     self.note.ticks_per_quarternote*8]

    map = MapPianoComp()

    self.note.length_maps = map.length_maps
    self.note.length_map_chooser = map.length_map_chooser

    self.note.max_simultaneous = 4
	
	# remove forbidden notes from all categories and the full note scope
    for category in self.note.categories:
      self.note.categories[category] = list(set(self.note.categories[category]) - set(self.note.forbidden_notes))
      self.note.scope = self.note.scope + self.note.categories[category]

    self.note.simultaneous_chance = lea.pmf({
      True: 0.75,
      False: 0.25
    })

    self.note.ticks_per_quarternote = 480 # can be up to 960

    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 6]
    self.phrase.record_chance = lea.pmf({
      True: 0.25,
      False: 0.75
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.4,
      False: 0.6
    })

    self.space = map.space

    self.use_randomized_tuning = False

    self.volume = VolumeConfig()

class PadPiano():
  def __init__(self):
    self.name = "Pad Piano"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = True
    self.note.scope = [21, 109]
    self.note.categories = {
      NoteCategory.LOW.value: list(range(self.note.scope[0], 60)),
      NoteCategory.MIDDLE.value: list(range(61, 70)),
      NoteCategory.HIGH.value: list(range(71, self.note.scope[1]))
    }
    self.note.chooser = lea.pmf({
      NoteCategory.LOW.value: 0.025,
      NoteCategory.MIDDLE.value: 0.95,
      NoteCategory.HIGH.value: 0.025,
    })
    self.note.count_scope = [200, 300]
    self.note.forbidden_notes = []
    self.note.length_scope = [self.note.ticks_per_quarternote, 
                     self.note.ticks_per_quarternote*2]
    self.note.max_simultaneous = 5
    self.note.scope = [21, 109]
    self.note.simultaneous_chance = lea.pmf({
      True: 0.75,
      False: 0.25
    })
    self.note.ticks_per_quarternote = 480 # can be up to 960

    self.phrase = PhraseConfig()
    self.phrase.count_scope = [5, 20]
    self.phrase.record_chance = lea.pmf({
      True: 0.5,
      False: 0.5
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.15,
      False: 0.85
    })

    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0.15,
      False: 0.85
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (2, 5)

    self.tempo = TempoConfig()
    self.tempo.change_chooser = lea.pmf({
      True: 0.1,
      False: 0.9
    })
    self.scope_chooser = lea.pmf(
    {
      0: 1
    })
    self.scopes = (
      (150, 200)
    )

    self.use_randomized_tuning = False
    self.volume_scope = [80, 100]

# this one works well for slow jazz.
# just needs adjustment to note.count_scope to fit with desired length.
class PianoLongChords():
  def __init__(self):
    self.name = "Piano Long Chords"
    self.debug_log = False
  
    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = True
    self.note.force_simultaneous_from_same_category = False
    self.note.scope = [21, 109]
    self.note.categories = {
      NoteCategory.LOW.value: list(range(self.note.scope[0], 55)),
      NoteCategory.MIDDLE.value: list(range(56, 75)),
      NoteCategory.HIGH.value: list(range(76, self.note.scope[1]))
    }
    self.note.chooser = lea.pmf({
      NoteCategory.LOW.value: 0.05,
      NoteCategory.MIDDLE.value: 0.8,
      NoteCategory.HIGH.value: 0.05,
    })
    self.note.count_scope = [7, 10]
    self.note.forbidden_notes = []
    self.note.length_scope = [self.note.ticks_per_quarternote*4, 
                     self.note.ticks_per_quarternote*32]

    self.note.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 20, (3, 5)),
      "Name1": build_tempo_length_map((1, 301), 20, (0.5, 5)),
     }
    self.note.length_map_chooser = lea.pmf({
      "Name0": 0.9,
      "Name1": 0.1,
    })

    self.note.max_simultaneous = 5
    self.note.simultaneous_chance = lea.pmf({
      True: 0.75,
      False: 0.25
    })
    self.note.ticks_per_quarternote = 480 # can be up to 960

    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 8]
    self.phrase.record_chance = lea.pmf({
      True: 0,
      False: 1
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0,
      False: 1
    })

    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0,
      False: 1
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (2, 5)

    self.use_randomized_tuning = False
    self.volume = VolumeConfig()

class PadSynth():
  def __init__(self):
    self.name = "Pad Synth"
    self.debug_log = False

    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = True
    self.note.force_simultaneous_from_same_category = False
    self.note.scope = [21, 109]
    self.note.categories = {
      NoteCategory.LOW.value: list(range(self.note.scope[0], 50)),
      NoteCategory.MIDDLE.value: list(range(51, 80)),
      NoteCategory.HIGH.value: list(range(81, self.note.scope[1]))
    }
    self.note.chooser = lea.pmf({
      NoteCategory.LOW.value: 0.025,
      NoteCategory.MIDDLE.value: 0.95,
      NoteCategory.HIGH.value: 0.025,
    })
    self.note.count_scope = [250, 500]
    self.note.forbidden_notes = []
    self.note.length_scope = [self.note.ticks_per_quarternote*2, self.note.ticks_per_quarternote*16]
    self.note.max_simultaneous = 5
    self.note.simultaneous_chance = lea.pmf({
      True: 0.90,
      False: 0.10
    })
    self.note.ticks_per_quarternote = 480 # can be up to 960

    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 10]
    self.phrase.record_chance = lea.pmf({
      True: 0,
      False: 1
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0,
      False: 1
    })

    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0,
      False: 1
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0, 0)

    self.tempo = TempoConfig()
    self.tempo.change_chooser = lea.pmf({
      True: 0.2,
      False: 0.8
    })
    self.scope_chooser = lea.pmf(
    {
      0: 1
    })
    self.scopes = (
      (60, 60)
    )

    self.use_randomized_tuning = False
    self.volume = VolumeConfig()

class Vibes():
  def __init__(self):
    self.name = "Vibes"
    self.debug_log = False
  
    self.note = NoteConfig()
    self.note.allow_simultaneous_from_same_category = True
    self.note.force_simultaneous_from_same_category = True
    self.note.scope = [21, 109]
    self.note.categories = {
      NoteCategory.LOW.value: list(range(self.note.scope[0], 50)),
      NoteCategory.MIDDLE.value: list(range(50, 86)),
      NoteCategory.HIGH.value: list(range(86, self.note.scope[1]))
    }
    self.note.chooser = lea.pmf({
      NoteCategory.LOW.value: 0,
      NoteCategory.MIDDLE.value: 1,
      NoteCategory.HIGH.value: 0,
    })
    self.note.count_scope = [250, 250]
    self.note.forbidden_notes = []
    self.note.length_scope = [self.note.ticks_per_quarternote*8, 
                     self.note.ticks_per_quarternote*16]

    self.note.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 9, (0.0625, 1.5)),
      "Name1": build_tempo_length_map((1, 301), 20, (0.25, 1.5)),
      "Name2": build_tempo_length_map((1, 301), 5, (1, 2))
      
      #"Name2": build_tempo_length_map((1, 301), 16, (2, 32))
      #"Name3": build_tempo_length_map((1, 301), 4, (0.125, 4))
     }
    self.note.length_map_chooser = lea.pmf({
      "Name0": 0.3,
      "Name1": 0.3,
      "Name2" : 0.4
    })
    
    self.note.max_simultaneous = 3
    self.note.scope = [21, 109]
    self.note.simultaneous_chance = lea.pmf({
      True: 0.4,
      False: 0.6
    })
    self.note.ticks_per_quarternote = 480 # can be up to 960

    self.phrase = PhraseConfig()
    self.phrase.count_scope = [3, 8]
    self.phrase.record_chance = lea.pmf({
      True: 0.15,
      False: 0.85
    })
    self.phrase.replay_chance = lea.pmf({
      True: 0.25,
      False: 0.75
    })

    self.space = SpaceConfig()
    self.space.chance = lea.pmf({
      True: 0.1,
      False: 0.9
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.5, 1)

    self.tempo = TempoConfig()
    self.tempo.change_chooser = lea.pmf({
      True: 0,
      False: 1
    })
    self.scope_chooser = lea.pmf(
    {
      0: 1
    })
    self.scopes = (
      (120, 120)
    )

    self.use_randomized_tuning = False
    self.volume_scope = [90, 110]

