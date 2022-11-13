import lea

class ConfigPhrase:
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
