import lea
from PyRM.configs.ConfigImprov import build_tempo_length_map
from PyRM.configs.ConfigSpace import ConfigSpace

class MapPianoOrnament():
  def __init__(self):
    self.name = "Piano Ornament"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 1, (0.003125, 0.0625)),
      "Name1": build_tempo_length_map((1, 301), 9, (0.0625, 0.25)),
      "Name2": build_tempo_length_map((1, 301), 5, (0.0625, 0.5)),
      "Name3": build_tempo_length_map((1, 301), 9, (0.0625, 1.5)),
      "Name4": build_tempo_length_map((1, 301), 9, (0.125, 0.25)),
      "Name5": build_tempo_length_map((1, 301), 9, (0.125, 0.5)),
      "Name6": build_tempo_length_map((1, 301), 9, (0.125, 1.5)),
      "Name7": build_tempo_length_map((1, 301), 5, (1, 2))
    }
     
    self.length_map_chooser = lea.pmf({
      "Name0": 0,
      "Name1": 0,
      "Name2": 0,
      "Name3": 1,
      "Name4": 0,
      "Name5": 0,
      "Name6": 0,
      "Name7": 0
    })

    self.space = ConfigSpace()
    self.space.chance = lea.pmf({
      False: 1,
      True: 0
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.05, 0.250)
