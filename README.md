# PyRM

PyRM is a tool that will allow you to create midi files with the potential for randomizing many properties, including number of notes, note length, note pitch, number of simultaneous notes, tempo changes, tuning changes, note categories with weighted probability, and more.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
midiutil
lea
```

## License

This project is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

See the [LICENSE.md](LICENSE.md) file for details

## What this thing does
* create pyrm object
  * configure logging
  * load config
  * initialize midi object
  * initialize track object
  * initialize list of recorded phrases
* build the track
  * initialize channel (always 0 right now)
  * initialize track_number (always 0 right now)
  * initialize note_start_time
  * initialize recording variables
    * record_index
    * phrase_count
  * generate the number of notes that the entire track will have
  * generate tuple of note categories. distribution will match up with config.note_config.chooser settings. number of notes generated will match with the number randomly generated in the previous step
  * set flag indicating whether to modify tempo randomly
  * set initial tempo (random if tempo modification enabled, otherwise use the first element in config.tempo_scope)
  * loop through the note categories tuple
    * if tempo changes are being used
      * set tempo_change_change to a random number within config.tempo_change_chance_range
      * if tempo_change_chance divided by config.tempo_change_chance is 0
        * add the tempo to the tempos dictionary for the track currently being built. The key is note_start_time and the tempo is the value
    * set volume to a randomly generated number based on config.volume_scope
    * set note_length to a randomly generated number based on config.note_config.length_scope
    * set pitch
      * if the specified config has config.note_config.chooser
        * select a note category (based on the note category distribution from config.note_config.chooser)
        * if working with the primary/first note
          * get a random pitch from the selected note category
        * else
          * get a random pitch from all possible notes to choose from (config.note_config.scope) TODO: Set this up so that it’s only picking from a complementary category
      * else
        * get a random pitch from all possible notes to choose from (config.note_config.scope)
    * if no phrases have been recorded
      * initialize the record_phrase flag to indicate whether recording should happen based on the probability distribution specified in config.phrase_record_chance
      * if recording a phrase
        * select a random number of notes to add to the phrase based on config.phrase_count_scope
        * initialize phrase_index and recorded_phrase
    * if recording a phrase
      * if there is still space to add more notes
        * increment the phrase index
      * else
        * initialize number of notes in a phrase and the phrase index to 0
        * add the currently recorded phrase to the list of recorded phrases
        * wipe out the recorded_phrase
        * set the record_phrase to False
    * add the note to the notes dictionary in the track currently being built
      * if the specified note start time doesn’t exist as a key in track.notes
        * using the specified note start time as a key, initialize a list as the value
      * append the note to the list for the specified note start time
      * if recording a phrase
        * add the note to the currently recording phrase with the current start time as the key. This start time should NOT be used when playing back a recording.
    * Add the current pitch to the simultaneous_pitches list
    * iterate on a range created from config.note_config.max_simultaneous
      * select a random choice to indicate whether a simultaneous note should be added (based on the distribution in config.note_config.simultaneous_change)
        * get a random pitch from all possible notes to choose from (config.note_config.scope) TODO: Set this up so that it’s only picking from a complementary category
        * if the note has already been added, break the loop to add simulatneous pitches
        * if the note is in the same category as the primary note, skip to the next loop iteration for generating a simultaneous pitch
        * else 
          * set note_length to a randomly generated number based on config.note_config.length_scope
          * add the note to the notes dictionary in the track currently being built
            * if the specified note start time doesn’t exist as a key in track.notes
              * using the specified note start time as a key, initialize a list as the value
            * append the note to the list for the specified note start time
            * if recording a phrase
              * add the note to the currently recording phrase with the current start time as the key. This start time should NOT be used when playing back a recording.
    * Set a new note_start_time based on the current note_start_time and note_length
      * set start_time_factor to a random number from config.note_config.start_time_factors
      * increment note_start_time by adding note_length / start_time_factor
    * Based on the config.phrase_replay_chance distribution, randomly select if we should replay a phrase
    * If we have decided to replay a phrase and we have some stored
      * Disable the flag that would allow recording to happen when adding a note
      * select a random phrase from track.recorded_phrases
      * for each chord in the phrase
        * for each note in the chord
          * add the note to the notes dictionary in the track currently being built
            * if the specified note start time doesn’t exist as a key in track.notes
              * using the specified note start time as a key, initialize a list as the value
            * append the note to the list for the specified note start time
      * Set a new note_start_time based on the current note_start_time and note_length
        * set start_time_factor to a random number from config.note_config.start_time_factors
        * increment note_start_time by adding note_length / start_time_factor
