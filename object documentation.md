# Note

## Properties

- length
  - default: 0
- pitch
  - default: 0
- volume
  - default: 0
- Notes
  - aka velocity, for midi

## Notes









# Phrase

## Properties

- chords
  - default: dict()
  - Notes
    - key is start_time, value is list() of Note objects

## Notes

- tempo of recorded notes not saved











# Track

## Properties

- config
  - default: object passed in
- format
  - default: None
- note_start_time
  - default: 0
  - Notes
    - tracks where next note goes
- notes
  - default: dict()
  - Notes
    - key is start_time, value is list of Note objects
- record_phrase
  - default: False
- recorded_phrases
  - default: list()
- tempos
  - default: dict()
  - Notes
    - key: start time
    - value: int representing tempo (1- ???)
- volumes
  - default: dict()
  - Notes
    - key: start time
    - value: int representing volume (0-127)

## Methods

- import_json
  - params
   - filename
- export_to_json_file   
  - params
   - customIdentifier
- add_note
- build_track
- pitch_category_used_in_simultaneous
- get_category_of_pitch
- calculate_note_start_time
- write_track
- _create_note
- _generate_pitch


## Notes

















# PyRM

## Properties
- currentTrack
  - default: None
- tracks
  - default: [] (empty list)
- midis
  - default: [] (empty list)
- config

## Methods

- build_tracks
- convert_tracks_to_midi_objects
- export_to_midi_files
- write_log
- _frequency
- _generate_randomized_tuning
- _load_config

## Static Methods
- get_int_or_float
- get_random
- get_random_from_list

## Notes




































# ConfigImprov

## Properties

- track_configs
  - default: [] (empty list)
- ticks_per_quarternote
  - default: 480
- tempo
  - default: ConfigTempo() in default state

## Methods

## Static Methods

- build_tempo_length_map

## Notes














# ConfigPhrase

## Properties

- count_scope
  - default: [5, 10]
- record_chance
  - default: probability map: False: 1, True: 0
- replay_chance
  - default: probability map: False: 1, True: 0

## Methods

## Static Methods

## Notes






# ConfigSpace

## Properties

- chance
  - default: probability map: False: 1, True: 0
- scope
  - default: tuple with single entry of 0

## Methods

## Static Methods

## Notes












# ConfigTempo

## Properties

- scope_change_chooser
  - default: False: 0.5, True: 0.5
  - probability of tempo scope change occurring
- change_chooser
  - default: False: 0.5, True: 0.5
  - probability of tempo change occurring
- scope_chooser
  - default:
    - 0: 0
    - 1: 0.25
    - 2: 0.25
    - 3: 0.25
    - 4: 0.25
  - maps tempo scopes to corresponding probabilities
- scopes
  - default
    - (50, 100)
    - (100, 150)
    - (150, 200)
    - (200, 250)
    - (250, 300)
  - defines tempo scope ranges


## Methods

## Static Methods

## Notes
- applies at the improv level, not the track level
















# ConfigVolume

## Properties

- scope_change_chooser
  - default: False: 0.5, True: 0.5
  - probability of volume scope change occurring
- change_chooser
  - default: False: 0.5, True: 0.5
  - probability of volume change occurring
- scope_chooser
  - default:
    - 0: 0
    - 1: 0.5
    - 2: 0.5
    - 3: 0
    - 4: 0
    - 5: 0

  - maps volume scopes to corresponding probabilities
- scopes
  - default
    - (0, 32)
    - (32, 64)
    - (64, 85)
    - (86, 96)
    - (97, 105)
    - (106, 127)
  - defines volume scope ranges


## Methods

## Static Methods

## Notes










# ConfigNoteBase

## Properties

- allow_simultaneous_from_same_category
  - default: False
- categories
  - default: {} - empty set
- chooser
- count_scope
  - default: [] - empty list
- forbidden_notes
- force_simultaneous_from_same_category
- length_maps
  - default: {} - empty set
- length_map_chooser
- length_scope
  - default: [] - empty list
- map
  - default: None
- max_simultaneous
  - default: 0
- scale_definitions
  - default: dictionary where key is a NoteCategory enum value and value is tuple of ints representing scale steps
  - examples
    - NoteCategory.CHROMATIC: (1,1,1,1,1,1,1,1,1,1,1,1)
    - NoteCategory.HARMONIC_MINOR: (2,1,2,2,1,3,1)
    - NoteCategory.HIRAJŌSHI: (2,1,4,1,4)
- scope
  - default: [] - empty list
- simultaneous_chance
  - default: False: 0, True: 1
- span_scope
  - default: [] - empty list
- ticks_per_quarternote
  - default: value passed in




## Methods

- generate_scale_notes
  - params
    - noteCategory
    - start
    - count


## Static Methods

## Notes














































