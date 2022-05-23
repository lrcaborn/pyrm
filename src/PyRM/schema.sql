CREATE TABLE note_category(
	id INTEGER PRIMARY KEY,
	category TEXT
);

CREATE TABLE config_session(
	id INTEGER PRIMARY KEY,
	ticks_per_quarternote INTEGER
);



CREATE TABLE config_tempo(
	id INTEGER PRIMARY KEY,
	config_session_id INTEGER,
	change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing tempo within the current scope.
	scope_change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing the tempo scope.
	FOREIGN KEY(config_session_id) REFERENCES config_session(id)
);

CREATE TABLE config_tempo_scope(
	id INTEGER PRIMARY KEY,
	config_tempo_id INTEGER,
	low INTEGER,
	high INTEGER,
	chance INTEGER,
	FOREIGN KEY(config_tempo_id) REFERENCES config_tempo(id)	
);



CREATE TABLE config_note(
	id INTEGER PRIMARY KEY,
	allow_simultaneous_from_same_category INTEGER, -- boolean 0 or 1
	force_simultaneous_from_same_category INTEGER, -- boolean 0 or 1
	format_change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing format.
	max_simultaneous INTEGER,
	simultaneous_chance INTEGER -- True value. False is 100 minus this valud. Likelihood of having simultaneous notes.
);

CREATE TABLE config_note_forbidden_note(
	config_note_id INTEGER,
	note_value INTEGER,
	PRIMARY KEY(config_note_id, note_value),
	FOREIGN KEY(config_note_id) REFERENCES config_note(id)	
);

CREATE TABLE config_note_length_scope(
	config_note_id INTEGER,
	low INTEGER,
	high INTEGER,
	FOREIGN KEY(config_note_id) REFERENCES config_note(id)
);

CREATE TABLE config_note_category(
	id INTEGER PRIMARY KEY,
	note_category_id INTEGER
);

CREATE TABLE config_note_category_note(
	config_note_category_id INTEGER,
	note_value INTEGER,
	FOREIGN KEY(config_note_category_id) REFERENCES config_note_category(id)
);

CREATE TABLE config_note_format(
	id INTEGER PRIMARY KEY,
	name TEXT,
	chance INTEGER -- True value. False value is 100 minus this value. Likelihood of choosing this format
);

CREATE TABLE config_note_format_definition(
	id INTEGER PRIMARY KEY,
	note_category_id INTEGER,
	chance INTEGER, -- True value. False value is 100 minus this value. Likeliood of a format being selected.
	FOREIGN KEY(note_category_id) REFERENCES note_category(id)
);



CREATE TABLE config_phrase(
	id INTEGER PRIMARY KEY,
	record_chance INTEGER, -- True value. False value is 100 minus this value. Likelihood of recording a phrase.
	replay_chance INTEGER-- True value. False value is 100 minus this value. Likelihood of select a phrase to replay.
);

CREATE TABLE config_phrase_count_scope(
	config_phrase_id INTEGER,
	low INTEGER,
	high INTEGER,
	FOREIGN KEY(config_phrase_id) REFERENCES config_phrase(id)
);


CREATE TABLE config_volume(
	id INTEGER PRIMARY KEY,
	config_session_id INTEGER,
	change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing tempo within the current scope.
	scope_change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing the tempo scope.
	FOREIGN KEY(config_session_id) REFERENCES config_session(id)
);

CREATE TABLE config_volume_scope(
	id INTEGER PRIMARY KEY,
	config_volume_id INTEGER,
	low INTEGER,
	high INTEGER,
	chance INTEGER,
	FOREIGN KEY(config_volume_id) REFERENCES config_volume(id)	
);
