#!/usr/bin/env python
import pprint
import argparse

from PyRM import PyRM, Config

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", "-f", help = "configuration to use", type = str, dest = "config_file")
parser.add_argument("--count", "-c", help = "number of files to create", type = str, dest = "file_count")
results = parser.parse_args()

config_file = results.config_file
file_count = int(results.file_count) or 5

for i in range(file_count):
    improv_config = Config.ImprovConfig()
    #improv_config.track_configs = [Config.DrumEzxJazz()]
    compPiano = Config.CompPiano()
    improv_config.track_configs = [compPiano, compPiano]
    #improv_config.track_configs = [Config.DrumEzxJazz()]
    #improv_config.track_configs = [Config.DrumEzxJazz(), Config.PadPiano()]
    #improv_config.track_configs = [Config.DrumEzxJazz(), Config.CompPiano(), Config.Vibes()]
    #improv_config.track_configs = [Config.PianoLongChords(), Config.Vibes()]
    pyrm = PyRM.PyRM(improv_config)
    pyrm.build_tracks()
    pyrm.convert_tracks_to_midi_objects()
    midi_file = pyrm.export_to_midi_files(str(i))
    #json_file = pyrm.export_to_json_file(str(i))
    pyrm.write_log()
