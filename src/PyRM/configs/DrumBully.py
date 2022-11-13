import PyRM.configs.NoteCategory
import PyRM.configs.ConfigVolume
    
class ConfigNote:
  def __init__(self):
    self.allow_simultaneous_from_same_category = False
    self.force_simultaneous_from_same_category = False
    
    self.categories = {
      NoteCategory.CRASH.value: [27, 28, 29, 30, 31, 32, 49, 52, 55, 57, 59], 
      NoteCategory.HAT.value: [16, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 62, 63, 64, 65], 
      NoteCategory.KICK.value: [36], 
      NoteCategory.RIDE.value: [51, 53], 
      NoteCategory.SNARE.value: [37, 38, 39, 40], 
      NoteCategory.TOM.value: [41, 43, 45, 47, 48, 50], 
    }

    self.count_scope = [1000, 1500]

    self.forbidden_notes = {17, 18, 19, 20, 33, 34, 35, 58, 61}

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
      False: 0.5,
      True: 0.5
    })

    self.ticks_per_quarternote = 480 # can be up to 960

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [3, 10]
    self.record_chance = lea.pmf({
      False: 0.8,
      True: 0.2
    })
    self.replay_chance = lea.pmf({
      False: 0.4,
      True: 0.6
    })

class DrumBully():
  def __init__(self):
    self.name = "BullyDrum"
    self.debug_log = False

    self.note = ConfigNote()
    
    self.phrase = ConfigPhrase()

    self.space = self.note.map.space
    
    self.use_randomized_tuning = False

    self.volume = ConfigVolume()


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
