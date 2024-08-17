from aenum import Flag, auto

class ClusterCategory(Flag):
    NONE = 0
    CRASH = auto()                      # "Cymbal Crash"
    HAT = auto()                        # "Hi-Hat"
    KICK = auto()                       # "Kick"
    RIDE = auto()                       # "Ride cymbal"
    SNARE = auto()                      # "Snare"
    TOM = auto()                        # "Tom"
   
    def __str__(self):
        return self.name
