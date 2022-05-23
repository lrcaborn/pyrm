#import math
import numpy
#in:
#	tempo_range tuple 
#	increment
#	modifier_range tuple
#out:
#	list of list of tuples like tempo length map now
	

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
        modifier = (modifiers[index], modifiers[index + 1])
        tempo_length_map.append((tempo, modifier))
        index += 1

    return tempo_length_map

build_tempo_length_map((1, 300), 7, (0.25, 8))


