import lea

class ConfigNote:
  def __init__(self):
    self.allow_simultaneous_from_same_category = False
    self.categories = {}
    self.chooser = None
    self.count_scope = []
    self.forbidden_notes = {}
    self.force_simultaneous_from_same_category = False
    self.length_maps = {}
    self.length_map_chooser = None
    self.length_scope = []
    self.map = None
    self.max_simultaneous = 0
    self.scope = []
    self.simultaneous_chance = lea.pmf({
      True: 1,
      False: 0
    })
    self.span_scope = []
    self.ticks_per_quarternote = 480
