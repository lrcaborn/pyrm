class MapPianoPad():
  def __init__(self):
    self.name = "Piano Pad"
    self.length_maps = {
      "Name0": build_tempo_length_map((1, 301), 20, (0.25, 1.5)),
      "Name1": build_tempo_length_map((1, 301), 5, (1, 2))
     }
    self.length_map_chooser = lea.pmf({
      "Name0": 1,
      "Name1": 0
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
    self.space.scope = (0.25, 1)
