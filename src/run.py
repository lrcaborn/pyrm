 #!/usr/bin/env python
import pprint
import argparse

from PyRM.PyRM import PyRM
from PyRM.configs import *

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", "-f", help="configuration to use", type=str, dest="config_file")
parser.add_argument("--count", "-c", default=1, help="number of files to create", type=int, dest="file_count")
results = parser.parse_args()

config_file = results.config_file
file_count = int(results.file_count)

for i in range(file_count):
  improv_config = ConfigImprov.ConfigImprov()
  improv_config.track_configs = [DrumEzxJazz.DrumEzxJazz(improv_config.ticks_per_quarternote)]
  #improv_config.track_configs = [Config.DrumBlues()]
  #improv_config.track_configs = [Config.DrumHell()]
  #improv_config.track_configs = [Config.DrumVintage1963()]
  #improv_config.track_configs = [Config.PianoLongNotes()]
  #improv_config.track_configs = [Config.PadPiano()]
  #improv_config.track_configs = [Config.OrnamentPiano()]
  #improv_config.track_configs = [Config.Drum808()]
  #improv_config.track_configs = [Config.CompPiano()]

  #improv_config.track_configs = [Config.Drum808()]
  #improv_config.track_configs = [Config.Vibes()]
  #improv_config.track_configs = [Config.DrumVintage1963()]
  
  #improv_config.track_configs = [Config.DrumEzxJazz(), Config.PadPiano()]
  #improv_config.track_configs = [Config.DrumEzxJazz(), Config.CompPiano(), Config.Vibes()]
  #improv_config.track_configs = [Config.PianoLongChords(), Config.Vibes()]
  pyrm = PyRM(improv_config)
  pyrm.build_tracks()
  pyrm.convert_tracks_to_midi_objects()
  midi_file = pyrm.export_to_midi_files(str(i))
  #json_file = pyrm.export_to_json_file(str(i))
  pyrm.write_log()
