import lea

class ConfigPhrase:
  def __init__(self):
    self.count_scope = [5, 10]
    self.record_chance = lea.pmf({
      False: 1,
      True: 0
    })
    self.replay_chance = lea.pmf({
      False: 1,
      True: 0
    })
