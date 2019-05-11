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
    #config = Config.ConfigPianoLongChords()
    #config = Config.ConfigDrumEzxJazzSlow()
    #config = Config.ConfigDrumEzxJazzMid()
    config = Config.ConfigDrumEzxJazzFast()
    #config = Config.ConfigCompPiano()
    #config = Config.ConfigPadPiano()

    pyrm = PyRM.PyRM(config)
    pyrm.build_track()
  
    #pprint.pprint(pyrm.phrases)
    pyrm.convert_track_to_midi()
    midi_file = pyrm.export_midi_file(str(i))
    json_file = pyrm.export_track_to_json_file(str(i))
    pyrm.write_log()
