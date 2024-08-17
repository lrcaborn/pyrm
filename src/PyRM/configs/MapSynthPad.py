import lea
from PyRM.configs.ConfigImprov import build_tempo_length_map
from PyRM.configs.ConfigSpace import ConfigSpace

class MapSynthPad():
  def __init__(self):
    self.name = "Synth Pad"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 20, (0.25, 1.5)),
      "Name1": build_tempo_length_map((1, 301), 5, (1, 15))
     }
    self.length_map_chooser = lea.pmf({
      "Name0": 0,
      "Name1": 1
    })

    self.space = ConfigSpace()
    self.space.chance = lea.pmf({
      True: 0.2,
      False: 0.8
    })
    # seconds, so will need to calculate
    # tempo = 180bpm
    # that's 180 / 60 beats per seconds
    # if we're using 480 ticks per quarter note, that's 
    # 480 * 3 = 1440 ticks
    # 1440 * rand # between 5 and 10 (let's say 7)
    # total tick count for this silence == 1440 * 7 == 10080
    self.space.scope = (0.25, 1)
