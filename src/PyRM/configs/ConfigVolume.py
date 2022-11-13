import lea

class ConfigVolume:
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
