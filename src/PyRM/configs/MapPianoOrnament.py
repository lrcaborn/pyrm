import lea
from PyRM.configs.ConfigImprov import build_tempo_length_map
from PyRM.configs.ConfigSpace import ConfigSpace

class MapPianoOrnament():
  def __init__(self):
    self.name = "Piano Ornament"
    self.length_maps = {
      #"Name0": build_tempo_length_map((1, 301), 1, (0.003125, 0.0625))
      "Name0": build_tempo_length_map((1, 301), 9, (0.0625, 0.25)),
      "Name1": build_tempo_length_map((1, 301), 5, (0.0625, 0.5)),
      "Name2": build_tempo_length_map((1, 301), 9, (0.0625, 1.5)),
      "Name3": build_tempo_length_map((1, 301), 9, (0.125, 0.25)),
      "Name4": build_tempo_length_map((1, 301), 9, (0.125, 0.5)),
      "Name5": build_tempo_length_map((1, 301), 9, (0.125, 1.5))
     }
    self.length_map_chooser = lea.pmf({
      "Name0": 0,
      "Name1": 1,
      "Name2": 0,
      "Name3": 0,
      "Name4": 0,
      "Name5": 0
    })

    self.space = ConfigSpace()
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
    self.space.scope = (0.25, 0.75)
