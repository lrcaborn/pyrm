from enum import Enum
import numpy
import lea

import PyRM

class ConfigImprov:
  def __init__(self):
    self.track_configs = []
    # for now we will set it here and overwrite whatever is in the 
    # individual config.note.ticks_per_quarternote var
    self.ticks_per_quarternote = 480

    self.tempo = PyRM.configs.ConfigTempo.ConfigTempo()
    self.tempo.scope_change_chooser = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.tempo.change_chooser = lea.pmf({
      False: 0.75,
      True: 0.25
    })
    self.tempo.scope_chooser = lea.pmf(
    {
      0: 0,
      1: 1,
      2: 0,
      3: 0,
      4: 0
    })
    self.tempo.scopes = (
      (50, 100),
      (100, 150),
      (150, 200),
      (200, 250),
      (250, 300)
    )

    #self.tempo.scope_chooser = lea.pmf(
    #{
    #  0: 1
    #})
    #self.tempo.scopes = [
    #  (50, 110)
    #]


    

    




#def calculate_modifier_end(modifier_start, modifier_adjustment):
#  return modifier_start * modifier_adjustment
#  #return modifier_start + (0.5 / modifier_adjustment)

# modifier 
# 1 = quarter note
# 0.25 = 16th note
# 8 = 2 measures	
def build_tempo_length_map(tempo_range, tempo_increment, modifier_range):
  tempo_length_map = []
  tempo_max = tempo_range[1]
  
  if tempo_max % tempo_increment != 0:
    tempo_max = tempo_range[1] + tempo_increment
  
  count = (tempo_max - tempo_range[0]) / tempo_increment
  modifier_increment = (modifier_range[1] - modifier_range[0]) / count
  
  tempos = numpy.arange(tempo_range[0], tempo_max, tempo_increment)
  modifiers = numpy.arange(modifier_range[0], modifier_range[1] + 0.0001, modifier_increment)
  
  index = 0
  
  while index < count - 1:
    tempo = (tempos[index], tempos[index + 1])
    modifier = (modifiers[0], modifiers[index + 1])
    tempo_length_map.append((tempo, modifier))
    index += 1

  return tempo_length_map




  


class blahConfig():
  def __init__(self):
    self.pattern = {
      NoteCategory.CRASH.value: (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      NoteCategory.HAT.value: (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
      NoteCategory.KICK.value: (1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0),
      NoteCategory.RIDE.value: (0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1),
      NoteCategory.SNARE.value: (0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0),
      NoteCategory.TOM.value: (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    }




    



    


