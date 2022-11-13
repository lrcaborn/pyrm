import lea

# this configuration applies at the improv level, not the track level
class ConfigTempo:
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
