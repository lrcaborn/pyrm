import lea

class ConfigSpace:
  def __init__(self):
    self.chance = lea.pmf({
      True: 0,
      False: 1
    })
    self.scope = (0,)
