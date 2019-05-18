from enum import Enum
import lea

class Category(Enum):
    # drums
    COWBELL = "Cowbell"
    CRASH = "Cymbal Crashes"
    HAT = "Hi-Hat"
    KICK = "Kick"
    RIDE = "Ride cymbal"
    SNARE = "Snare"
    TOM = "Toms"

    # piano sections
    LOW = "Low"
    MIDDLE = "Middle"
    HIGH = "High"
    
    def __str__(self):
        return self.name

class NoteConfig:
    def __init__(self):
        self.categories = {}
        self.count_scope = []
        self.forbidden_notes = {}
        self.length_scope = []
        self.max_simultaneous = 0
        self.scope = []
        self.simultaneous_chance = lea.pmf({
            True: 1,
            False: 0
        })
        self.span_scope = []
        self.ticks_per_quarternote = 480
    
class TempoConfig:
    def __init__(self):
        pass

class ConfigBase:
    def __init__(self):
        self.name = "Base"

        self.note_config = NoteConfig()
        self.note_config.allow_simultaneous_from_same_category = False
        self.note_config.count_scope = [100, 1000]
        self.note_config.length_scope = [1, self.note_config.ticks_per_quarternote*4]
        self.note_config.max_simultaneous = 3
        self.note_config.scope = [21, 108] # A0 to C8
        self.note_config.simultaneous_chance = lea.pmf({
            True: 0.25,
            False: 0.75
        })
        self.note_config.ticks_per_quarternote = 480 # can be up to 960
        
        self.phrase_count_scope = [3, 10]
        self.phrase_record_chance = lea.pmf({
            True: 0,
            False: 1
        })
        self.phrase_replay_chance = lea.pmf({
            True: 0,
            False: 1
        })
        
        self.tempo_change_chance = 2
        self.tempo_change_chance_range = [1, 100]
        self.tempo_scope = [30, 200]

        self.use_randomized_tuning = False
        self.volume_scope = [1, 127]
        
    @classmethod
    def getStats(self):
        print(self.note_config.chooser)
        print(self.note_config.simultaneous_chance)


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
    
class ConfigDrumBullySlow(ConfigDrumBully):
    def __init__(self):
        super().__init__()

        self.name = "BullyDrumSlow"
        self.debug_log = True

        self.note_config.categories = {
            Category.HAT.value: [16, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 62, 63, 64, 65], 
            Category.CYMBAL_CRASHES.value: [27, 28, 29, 30, 31, 32, 49, 52, 55, 57, 59], 
            Category.KICK.value: [36], 
            Category.SNARE.value: [37, 38, 39, 40], 
            Category.TOM.value: [41, 43, 45, 47, 48, 50], 
            Category.RIDE_CYMBAL.value: [51, 53], 
            Category.COWBELL.value: [54, 56]
        }
        self.note_config.chooser = lea.pmf({
            Category.COWBELL.value: 0.05,
            Category.CYMBAL_CRASHES.value: 0,
            Category.HAT.value: 0.15,
            Category.KICK.value: 0.30,
            Category.RIDE_CYMBAL.value: 0.15,
            Category.SNARE.value: 0.25,
            Category.TOM.value: 0.10
        })
        self.note_config.count_scope = [100, 100]
        self.note_config.forbidden_notes = {17, 18, 19, 20, 33, 34, 35, 58, 61}
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote/8, self.note_config.ticks_per_quarternote]
        self.note_config.max_simultaneous = 3
        self.note_config.scope = list(set(range(16, 65)) - self.note_config.forbidden_notes)

        self.tempo_scope = [40, 70]
        self.volume_scope = [90, 127]

class ConfigDrumBullyFast():
    def __init__(self):
        super().__init__()

        self.name = "BullyDrumFast"
        self.debug_log = True

        self.note_config.categories = {
            Category.HAT.value: [16, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 62, 63, 64, 65], 
            Category.CYMBAL_CRASHES.value: [27, 28, 29, 30, 31, 32, 49, 52, 55, 57, 59], 
            Category.KICK.value: [36], 
            Category.SNARE.value: [37, 38, 39, 40], 
            Category.TOM.value: [41, 43, 45, 47, 48, 50], 
            Category.RIDE_CYMBAL.value: [51, 53], 
            Category.COWBELL.value: [54, 56]
        }
        self.note_config.chooser = lea.pmf({
            Category.COWBELL.value: 0.05,
            Category.CYMBAL_CRASHES.value: 0,
            Category.HAT.value: 0.15,
            Category.KICK.value: 0.30,
            Category.RIDE_CYMBAL.value: 0.15,
            Category.SNARE.value: 0.25,
            Category.TOM.value: 0.10
        })
        self.note_config.count_scope = [1000, 1500]
        self.note_config.forbidden_notes = {17, 18, 19, 20, 33, 34, 35, 58, 61}
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote/2, self.note_config.ticks_per_quarternote]
        self.note_config.scope = list(set(range(16, 65)) - self.note_config.forbidden_notes)

        self.tempo_scope = [150, 180]
        self.volume_scope = [90, 127]

class ConfigOrnament(ConfigBase):
    def __init__(self):
        super().__init__()
        self.name = "Ornament"
        self.note_config.count_scope = [100, 200]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote/4, self.note_config.ticks_per_quarternote]
        self.note_config.max_simultaneous = 4
        self.note_config.scope = [0, 127]
        self.volume_scope = [80, 100]
        self.tempo_scope = [30, 300]

class ConfigDrumEzxJazz(ConfigDrum):
    def __init__(self):
        super().__init__()

        self.name = "EzxJazz"
        self.debug_log = True
        
        self.note_config.categories = {
            Category.HAT.value: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 61, 62, 63, 64, 65, 119, 120, 121, 122, 123, 124], 
            Category.KICK.value: [34, 35, 36], 
            Category.RIDE.value: [30, 31, 32, 51, 52, 53, 57, 58, 59, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118], 
            Category.SNARE.value: [6, 33, 38, 39, 40, 66, 67, 68, 69, 70, 71, 125, 126, 127], 
            Category.CRASH.value: [27, 28, 29, 49, 54, 55, 83, 94, 95], 
            Category.TOM.value: [4, 5, 41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
        }
        self.note_config.chooser = lea.pmf({
            Category.CRASH.value: 0,
            Category.HAT.value: 0.15,
            Category.KICK.value: 0.30,
            Category.RIDE.value: 0.15,
            Category.SNARE.value: 0.25,
            Category.TOM.value: 0.10
        })
        self.note_config.count_scope = [1000, 1500]
        self.note_config.forbidden_notes = {1, 2, 3, 37, 56, 76} # 37 is sidestick
        self.note_config.scope = list(set(range(0, 128)) - self.note_config.forbidden_notes)
        self.note_config.simultaneous_chance = lea.pmf({
            True: 0.3,
            False: 0.7
        })

        self.phrase_count_scope = [3, 5]
        self.phrase_record_chance = lea.pmf({
            True: 0.75,
            False: 0.25
        })
        self.phrase_replay_chance = lea.pmf({
            True: 0.25,
            False: 0.75
        })

        self.tempo_change_chance_range = [0, 100]
        self.tempo_change_chance = 10

class ConfigDrumEzxJazzSlow(ConfigDrumEzxJazz):
    def __init__(self):
        super().__init__()

        self.name = "EzxJazzSlow"
        self.debug_log = True

        self.note_config.chooser = lea.pmf({
            Category.CRASH.value: 0,
            Category.HAT.value: 0.2,
            Category.KICK.value: 0.35,
            Category.RIDE.value: 0,
            Category.SNARE.value: 0.3,
            Category.TOM.value: 0.15
        })
        self.note_config.count_scope = [1000, 1200]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote/2, 
                                         self.note_config.ticks_per_quarternote]
        self.start_time_factors = tuple(range(2, 3))
        self.tempo_scope = [60, 120]

class ConfigDrumEzxJazzMid(ConfigDrumEzxJazz):
    def __init__(self):
        super().__init__()

        self.name = "EzxJazzMid"
        self.debug_log = True

        self.note_config.count_scope = [600, 1000]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote, 
                                         self.note_config.ticks_per_quarternote*2]
        self.start_time_factors = tuple(range(1, 2))
        self.tempo_scope = [120, 180]

class ConfigDrumEzxJazzFast(ConfigDrumEzxJazz):
    def __init__(self):
        super().__init__()

        self.name = "EzxJazzFast"
        self.debug_log = True

        self.note_config.chooser = lea.pmf({
            Category.CRASH.value: 0,
            Category.HAT.value: 0.1,
            Category.KICK.value: 0.4,
            Category.RIDE.value: 0.1,
            Category.SNARE.value: 0.25,
            Category.TOM.value: 0.15
        })
        self.note_config.count_scope = [2000, 2000]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote*2, 
                                         self.note_config.ticks_per_quarternote*4]
        self.note_config.start_time_factors = (tuple(range(-1, 0)) 
                                               + tuple(range(1, 3)))
        self.tempo_scope = [180, 220]

class ConfigOrnamentPiano(ConfigOrnament):
    def __init__(self):            
        super().__init__()

        self.name = "OrnamentPiano"
        self.debug_log = True

        self.note_config.scope = [21, 109]
        self.note_config.categories = {
            Category.LOW.value: list(range(self.note_config.scope[0], 56)),
            Category.HIGH.value: list(range(57, self.note_config.scope[1]))
        }
        self.note_config.chooser = lea.pmf({
            Category.LOW.value: 0.15,
            Category.HIGH.value: 0.85,
        })
        self.note_config.count_scope = [15, 25]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote/2, 
                                         self.note_config.ticks_per_quarternote]
        self.note_config.max_simultaneous = 4
        
        self.start_time_factors = tuple(range(1, 5))
        self.tempo_change_chance = 10
        self.tempo_change_chance_range = [0, 100]
        self.tempo_scope = [200, 250]
        self.volume_scope = [80, 100]

class ConfigPiano(ConfigBase):
    def __init__(self):
        super().__init__()

        self.name = "Piano"
        self.debug_log = True

        self.note_config.allow_simultaneous_from_same_category = True
        self.note_config.categories = {
            Category.LOW.value: list(range(self.note_config.scope[0], 60)),
            Category.MIDDLE.value: list(range(61, 70)),
            Category.HIGH.value: list(range(71, self.note_config.scope[1]))
        }
        self.note_config.chooser = lea.pmf({
            Category.LOW.value: 0.025,
            Category.MIDDLE.value: 0.95,
            Category.HIGH.value: 0.025,
        })
        self.note_config.scope = [21, 109]
        self.note_config.simultaneous_chance = lea.pmf({
            True: 0.85,
            False: 0.15
        })

        self.phrase_count_scope = [5, 20]
        self.phrase_record_chance = lea.pmf({
            True: 0.3,
            False: 0.7
        })
        self.phrase_replay_chance = lea.pmf({
            True: 0.15,
            False: 0.85
        })

        self.tempo_change_chance = 10
        self.tempo_change_chance_range = [0, 100]

        self.volume_scope = [80, 100]

class ConfigCompPiano(ConfigPiano):
    def __init__(self):
        super().__init__()

        self.name = "Comp Piano"
        self.debug_log = True
    
        self.note_config.count_scope = [50, 100]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote, 
                                         self.note_config.ticks_per_quarternote*6]
        self.note_config.max_simultaneous = 2
        self.note_config.start_time_factors = tuple(range(-5, 0))

        self.tempo_scope = [80, 120]

class ConfigPadPiano(ConfigPiano):
    def __init__(self):
        super().__init__()

        self.name = "Pad Piano"
        self.debug_log = True

        self.note_config.count_scope = [50, 100]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote, 
                                         self.note_config.ticks_per_quarternote*4]
        self.note_config.max_simultaneous = 5
        self.note_config.start_time_factors = tuple(range(-5, 0))

        self.tempo_scope = [150, 200]

class ConfigPianoLongChords(ConfigPiano):
    def __init__(self):
        super().__init__()

        self.name = "Piano Long Chords"
        self.debug_log = True
    
        self.note_config.chooser = lea.pmf({
            Category.LOW.value: 0.005,
            Category.MIDDLE.value: 0.99,
            Category.HIGH.value: 0.005,
        })
        self.note_config.count_scope = [1000, 1000]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote/2, 
                                         self.note_config.ticks_per_quarternote*4]
        self.note_config.max_simultaneous = 3
        self.note_config.simultaneous_chance = lea.pmf({
            True: 0.90,
            False: 0.1
        })
        self.note_config.start_time_factors = tuple(range(-500, 0))
        self.tempo_change_chance = 0
        self.tempo_change_chance_range = [0,0]
        self.tempo_scope = [60, 60]
        self.volume_scope = [90, 110]

class ConfigPadSynth(ConfigBase):
    def __init__(self):
        super().__init__()

        self.name = "Pad Synth"
        self.debug_log = True

        self.note_config.scope = [21, 109]
        self.note_config.categories = {
            Category.LOW.value: list(range(self.note_config.scope[0], 50)),
            Category.MIDDLE.value: list(range(51, 80)),
            Category.HIGH.value: list(range(81, self.note_config.scope[1]))
        }
        self.note_config.chooser = lea.pmf({
            Category.LOW.value: 0.025,
            Category.MIDDLE.value: 0.95,
            Category.HIGH.value: 0.025,
        })
        self.note_config.count_scope = [250, 500]
        self.note_config.length_scope = [self.note_config.ticks_per_quarternote*2, self.note_config.ticks_per_quarternote*16]
        self.note_config.max_simultaneous = 5
        self.note_config.simultaneous_chance = lea.pmf({
            True: 0.90,
            False: 0.10
        })
        self.note_config.start_time_factors = tuple(range(-5, 0))
        self.tempo_scope = [60, 60]
        self.tempo_change_chance = 5
        self.tempo_change_chance_range = [0, 100]
        self.volume_scope = [80, 100]

