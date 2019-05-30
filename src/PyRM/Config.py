from enum import Enum
import lea

class NoteCategory(Enum):
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

class ImprovConfig:
    def __init__(self):
        self.track_configs = []
        # for now we will set it here and overwrite whatever is in the 
        # individual config.note.ticks_per_quarternote var
        self.ticks_per_quarternote = 480

        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.05,
            False: 0.95
        })
        self.tempo.scope = [150, 200]

class NoteConfig:
    def __init__(self):
        self.categories = {}
        self.chooser = None
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
        self.change_chooser = lea.pmf({
            True: 0,
            False: 1
        })
        self.scope = [60, 60]

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
    
class DrumBullySlow():
    def __init__(self):
        self.name = "BullyDrumSlow"
        self.debug_log = False

        self.note = NoteConfig()
        self.note.allow_simultaneous_from_same_category = False
        self.note.categories = {
            NoteCategory.HAT.value: [16, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 62, 63, 64, 65], 
            NoteCategory.CYMBAL_CRASHES.value: [27, 28, 29, 30, 31, 32, 49, 52, 55, 57, 59], 
            NoteCategory.KICK.value: [36], 
            NoteCategory.SNARE.value: [37, 38, 39, 40], 
            NoteCategory.TOM.value: [41, 43, 45, 47, 48, 50], 
            NoteCategory.RIDE_CYMBAL.value: [51, 53], 
            NoteCategory.COWBELL.value: [54, 56]
        }
        self.note.chooser = lea.pmf({
            NoteCategory.COWBELL.value: 0.05,
            NoteCategory.CYMBAL_CRASHES.value: 0,
            NoteCategory.HAT.value: 0.15,
            NoteCategory.KICK.value: 0.30,
            NoteCategory.RIDE_CYMBAL.value: 0.15,
            NoteCategory.SNARE.value: 0.25,
            NoteCategory.TOM.value: 0.10
        })
        self.note.count_scope = [100, 100]
        self.note.forbidden_notes = {17, 18, 19, 20, 33, 34, 35, 58, 61}
        self.note.length_scope = [self.note.ticks_per_quarternote/8, self.note.ticks_per_quarternote]
        self.note.max_simultaneous = 3
        self.note.scope = list(set(range(16, 65)) - self.note.forbidden_notes)
        self.note.simultaneous_chance = lea.pmf({
            True: 0.25,
            False: 0.75
        })
        self.note.start_time_factors = ()
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
        
        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.5,
            False: 0.5
        })
        self.tempo.scope = [40, 70]

        self.use_randomized_tuning = False
        self.volume_scope = [90, 127]

class DrumBullyFast():
    def __init__(self):
        self.name = "BullyDrumFast"
        self.debug_log = False

        self.note = NoteConfig()
        self.note.allow_simultaneous_from_same_category = False
        self.note.categories = {
            NoteCategory.HAT.value: [16, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 62, 63, 64, 65], 
            NoteCategory.CYMBAL_CRASHES.value: [27, 28, 29, 30, 31, 32, 49, 52, 55, 57, 59], 
            NoteCategory.KICK.value: [36], 
            NoteCategory.SNARE.value: [37, 38, 39, 40], 
            NoteCategory.TOM.value: [41, 43, 45, 47, 48, 50], 
            NoteCategory.RIDE_CYMBAL.value: [51, 53], 
            NoteCategory.COWBELL.value: [54, 56]
        }
        self.note.chooser = lea.pmf({
            NoteCategory.COWBELL.value: 0.05,
            NoteCategory.CYMBAL_CRASHES.value: 0,
            NoteCategory.HAT.value: 0.15,
            NoteCategory.KICK.value: 0.30,
            NoteCategory.RIDE_CYMBAL.value: 0.15,
            NoteCategory.SNARE.value: 0.25,
            NoteCategory.TOM.value: 0.10
        })
        self.note.count_scope = [1000, 1500]
        self.note.forbidden_notes = {17, 18, 19, 20, 33, 34, 35, 58, 61}
        self.note.length_scope = [self.note.ticks_per_quarternote/2, self.note.ticks_per_quarternote]
        self.note.max_simultaneous = 3
        self.note.scope = list(set(range(16, 65)) - self.note.forbidden_notes)
        self.note.simultaneous_chance = lea.pmf({
            True: 0.25,
            False: 0.75
        })
        self.note.start_time_factors = ()
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
        
        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.5,
            False: 0.5
        })
        self.tempo.scope = [150, 180]

        self.use_randomized_tuning = False
        self.volume_scope = [90, 127]

class DrumEzxJazz():
    def __init__(self):
        self.name = "EzxJazzFast"
        self.debug_log = False

        self.note = NoteConfig()
        self.note.allow_simultaneous_from_same_category = False
        self.note.categories = {
            NoteCategory.HAT.value: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 42, 44, 46, 60, 61, 62, 63, 64, 65, 119, 120, 121, 122, 123, 124], 
            NoteCategory.KICK.value: [34, 35, 36], 
            NoteCategory.RIDE.value: [30, 31, 32, 51, 52, 53, 57, 58, 59, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118], 
            NoteCategory.SNARE.value: [6, 33, 38, 39, 40, 66, 67, 68, 69, 70, 71, 125, 126, 127], 
            NoteCategory.CRASH.value: [27, 28, 29, 49, 54, 55, 83, 94, 95], 
            NoteCategory.TOM.value: [4, 5, 41, 43, 45, 47, 48, 50, 72, 73, 74, 75, 77, 78, 79, 80, 81, 82]
        }
        self.note.chooser = lea.pmf({
            NoteCategory.CRASH.value: 0,
            NoteCategory.HAT.value: 0.05,
            NoteCategory.KICK.value: 0.5,
            NoteCategory.RIDE.value: 0.05,
            NoteCategory.SNARE.value: 0.3,
            NoteCategory.TOM.value: 0.1
        })
        self.note.count_scope = [400, 600]
        self.note.forbidden_notes = {1, 2, 3, 37, 56, 76} # 37 is sidestick
        self.note.length_scope = [self.note.ticks_per_quarternote*8, 
                                         self.note.ticks_per_quarternote*16]
        self.note.max_simultaneous = 3
        self.note.scope = list(set(range(0, 128)) - self.note.forbidden_notes)
        self.note.simultaneous_chance = lea.pmf({
            True: 0.5,
            False: 0.5
        })
        self.note.start_time_factors = (tuple(range(-1, 0)) 
                                               + tuple(range(1, 3)))
        self.note.ticks_per_quarternote = 480 # can be up to 960
        
        self.phrase = PhraseConfig()
        self.phrase.count_scope = [3, 10]
        self.phrase.record_chance = lea.pmf({
            True: 0.25,
            False: 0.75
        })
        self.phrase.replay_chance = lea.pmf({
            True: 0.1,
            False: 0.9
        })
        
        self.space = SpaceConfig()
        self.space.chance = lea.pmf({
            True: 0.025,
            False: 0.975
        })
        # seconds, so will need to calculate
        # tempo = 180bpm
        # that's 180 / 60 beats per seconds
        # if we're using 480 ticks per quarter note, that's 
        # 480 * 3 = 1440 ticks
        # 1440 * rand # between 5 and 10 (let's say 7)
        # total tick count for this silence == 1440 * 7 == 10080
        self.space.scope = (2, 3)

        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.01,
            False: 0.99
        })
        self.tempo.scope = [100 , 220]

        self.use_randomized_tuning = False
        self.volume_scope = [80, 110]

class OrnamentPiano():
    def __init__(self):
        self.name = "OrnamentPiano"
        self.debug_log = False

        self.note = NoteConfig()
        self.note.allow_simultaneous_from_same_category = False
        self.note.scope = [21, 109]
        self.note.categories = {
            NoteCategory.LOW.value: list(range(self.note.scope[0], 56)),
            NoteCategory.HIGH.value: list(range(57, self.note.scope[1]))
        }
        self.note.chooser = lea.pmf({
            NoteCategory.LOW.value: 0.2,
            NoteCategory.HIGH.value: 0.8,
        })
        self.note.count_scope = [100, 100]
        self.note.forbidden_notes = []
        self.note.length_scope = [self.note.ticks_per_quarternote, 
                                         self.note.ticks_per_quarternote*2]
        self.note.max_simultaneous = 4
        self.note.simultaneous_chance = lea.pmf({
            True: 0.25,
            False: 0.75
        })
        self.note.start_time_factors = tuple(range(1, 5))
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
            True: 0.75,
            False: 0.25
        })
        # seconds, so will need to calculate
        # tempo = 180bpm
        # that's 180 / 60 beats per seconds
        # if we're using 480 ticks per quarter note, that's 
        # 480 * 3 = 1440 ticks
        # 1440 * rand # between 5 and 10 (let's say 7)
        # total tick count for this silence == 1440 * 7 == 10080
        self.space.scope = (1, 3)

        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.1,
            False: 0.9
        })
        self.tempo.scope = [200, 250]

        self.use_randomized_tuning = False
        self.volume_scope = [80, 100]

class CompPiano():
    def __init__(self):
        self.name = "Comp Piano"
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
        self.note.count_scope = [75, 125]
        self.note.length_scope = [self.note.ticks_per_quarternote, 
                                         self.note.ticks_per_quarternote*6]
        self.note.max_simultaneous = 2
        self.note.simultaneous_chance = lea.pmf({
            True: 0.85,
            False: 0.15
        })
        self.note.start_time_factors = tuple(range(-5, 0))
        self.note.ticks_per_quarternote = 480 # can be up to 960

        self.phrase = PhraseConfig()
        self.phrase.count_scope = [5, 20]
        self.phrase.record_chance = lea.pmf({
            True: 0.3,
            False: 0.7
        })
        self.phrase.replay_chance = lea.pmf({
            True: 0.15,
            False: 0.85
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
        self.space.scope = (1, 2)

        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.1,
            False: 0.9
        })
        self.tempo.scope = [80, 120]

        self.use_randomized_tuning = False
        self.volume_scope = [80, 100]

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
        self.note.start_time_factors = tuple(range(-3, 0))
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
        self.tempo.scope = [150, 200]

        self.use_randomized_tuning = False
        self.volume_scope = [80, 100]

class PianoLongChords():
    def __init__(self):
        self.name = "Piano Long Chords"
        self.debug_log = False
    
        self.note = NoteConfig()
        self.note.allow_simultaneous_from_same_category = True
        self.note.categories = {
            NoteCategory.LOW.value: list(range(self.note.scope[0], 60)),
            NoteCategory.MIDDLE.value: list(range(61, 70)),
            NoteCategory.HIGH.value: list(range(71, self.note.scope[1]))
        }
        self.note.chooser = lea.pmf({
            NoteCategory.LOW.value: 0.005,
            NoteCategory.MIDDLE.value: 0.99,
            NoteCategory.HIGH.value: 0.005,
        })
        self.note.count_scope = [1000, 1000]
        self.note.forbidden_notes = []
        self.note.length_scope = [self.note.ticks_per_quarternote/2, 
                                         self.note.ticks_per_quarternote*4]
        self.note.max_simultaneous = 3
        self.note.scope = [21, 109]
        self.note.simultaneous_chance = lea.pmf({
            True: 0.90,
            False: 0.1
        })
        self.note.start_time_factors = tuple(range(-500, 0))
        self.note.ticks_per_quarternote = 480 # can be up to 960

        self.phrase = PhraseConfig()
        self.phrase.count_scope = [5, 20]
        self.phrase.record_chance = lea.pmf({
            True: 0.3,
            False: 0.7
        })
        self.phrase.replay_chance = lea.pmf({
            True: 0.15,
            False: 0.85
        })

        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0,
            False: 1
        })
        self.tempo.scope = [60, 60]

        self.use_randomized_tuning = False
        self.volume_scope = [90, 110]

class PadSynth():
    def __init__(self):
        self.name = "Pad Synth"
        self.debug_log = False

        self.note = NoteConfig()
        self.note.allow_simultaneous_from_same_category = False
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
        self.note.scope = [21, 109]
        self.note.simultaneous_chance = lea.pmf({
            True: 0.90,
            False: 0.10
        })
        self.note.start_time_factors = tuple(range(-5, 0))
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

        self.tempo = TempoConfig()
        self.tempo.change_chooser = lea.pmf({
            True: 0.2,
            False: 0.8
        })
        self.tempo.scope = [60, 60]

        self.use_randomized_tuning = False
        self.volume_scope = [80, 100]
