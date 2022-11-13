CREATE TABLE note_category(
	id INTEGER PRIMARY KEY,
	category TEXT
);
-- drums
INSERT INTO config_note_category 
	(note_category_id) 
VALUES 
	-- drums
	('Cowbell'),
	('Cymbal Crash'),
	('HiHat'),
	('Kick'),
	('Ride'),
	('Snare'),
	('Tom'),
	('FX'),
	-- piano
	('Low'),
	('Middle'),
	('High'),
  	('AHarmonicMinor'),
  	('Japanese');




CREATE TABLE default_name(
	table_name TEXT,
	name TEXT
);
INSERT INTO default_names 
	(table_name, name) 
VALUES 
	('config_session', 'Default session'),
	('config_tempo', 'Default tempo'),
	('config_tempo_scope', 'Default tempo scope'),
	('config_note', 'Default note'),
	('config_note_format', 'Default note format');
	('config_volume', 'Default volume')




CREATE TABLE config_session(
	id INTEGER PRIMARY KEY,
	name TEXT,
	ticks_per_quarternote INTEGER
);
INSERT INTO config_session 
	(name, ticks_per_quarternote) 
VALUES 
	((SELECT name FROM default_name WHERE table_name = 'config_session'), 480);




CREATE TABLE config_tempo(
	id INTEGER PRIMARY KEY,
	name TEXT,
	config_session_id INTEGER,
	change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing tempo within the current scope.
	scope_change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing the tempo scope.
	FOREIGN KEY(config_session_id) REFERENCES config_session(id)
);
INSERT INTO config_tempo 
	(name, config_session_id, change_chance, scope_change_chance) 
VALUES 
	(
		(SELECT name FROM default_name WHERE table_name = 'config_tempo'), 
		(SELECT id FROM config_session WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_session')), 
		50, 50
	);




CREATE TABLE config_tempo_scope(
	id INTEGER PRIMARY KEY,
	name TEXT,
	config_tempo_id INTEGER,
	low INTEGER,
	high INTEGER,
	chance INTEGER,
	FOREIGN KEY(config_tempo_id) REFERENCES config_tempo(id)	
);
INSERT INTO config_tempo_scope 
	(name, config_tempo_id, low, high, chance) 
VALUES 
	(
		'Tempo Scope 1', 
		(SELECT id FROM config_tempo WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_tempo')), 
		50, 100, 5
	),
	(
		'Tempo Scope 2', 
		(SELECT id FROM config_tempo WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_tempo')), 
		100, 150, 30
	),
	(
		'Tempo Scope 3', 
		(SELECT id FROM config_tempo WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_tempo')), 
		150, 200, 50
	),
	(
		'Tempo Scope 4', 
		(SELECT id FROM config_tempo WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_tempo')), 
		200, 250, 15
	),
	(
		'Tempo Scope 5', 
		(SELECT id FROM config_tempo WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_tempo')), 
		250, 300, 0
	);


CREATE TABLE config_note(
	id INTEGER PRIMARY KEY,
	name TEXT,
	allow_simultaneous_from_same_category INTEGER, -- boolean 0 or 1
	force_simultaneous_from_same_category INTEGER, -- boolean 0 or 1
	format_change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing format.
	max_simultaneous INTEGER,
	simultaneous_chance INTEGER, -- True value. False is 100 minus this valud. Likelihood of having simultaneous notes.
	count_scope_low INTEGER,
	count_scope_high INTEGER,
	length_scope_low INTEGER,
	length_scope_high INTEGER
);
INSERT INTO config_note 
	(
		name, 
		allow_simultaneous_from_same_category, force_simultaneous_from_same_category, 
		format_change_chance, max_simultaneous, simultaneous_chance, 
		count_scope_low, count_scope_high, 
		length_scope_low, length_scope_high
	) 
	VALUES 
	(
		(SELECT name FROM default_name WHERE table_name = 'config_note'), 
		0, 0, 
		50, 3, 50, 
		100, 350,
		(SELECT ticks_per_quarternote * 16 FROM config_session WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_session')),
		(SELECT ticks_per_quarternote * 32 FROM config_session WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_session'))
	);




CREATE TABLE config_note_forbidden_note(
	config_note_id INTEGER,
	note_value INTEGER,
	PRIMARY KEY(config_note_id, note_value),
	FOREIGN KEY(config_note_id) REFERENCES config_note(id)	
);
INSERT INTO config_note_forbidden_note 
	(config_note_id, note_value) 
VALUES 
	((SELECT id FROM config_note WHERE name = 'Config Note 1'), 37);




CREATE TABLE config_note_category(
	id INTEGER PRIMARY KEY,
	note_category_id INTEGER
);
INSERT INTO config_note_category (note_category_id) 
SELECT id FROM note_category WHERE category IN ('Cymbal Crash', 'HiHat', 'Kick', 'Ride', 'Snare', 'Tom')


CREATE TABLE config_note_category_note(
	config_note_category_id INTEGER,
	note_value INTEGER,
	FOREIGN KEY(config_note_category_id) REFERENCES config_note_category(id)
);
INSERT INTO config_note_category_note 
	(config_note_category_note_id, note_value) 
VALUES 
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Cymbal Crash'), 48),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Cymbal Crash'), 49),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Cymbal Crash'), 56),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Cymbal Crash'), 57),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 42),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 44),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 45),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 46),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 52),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 54),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 55),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 58),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 59),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 60),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 61),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 62),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 63),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'HiHat'), 64),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Kick'), 36),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Ride'), 50),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Ride'), 51),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Ride'), 53),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Snare'), 38),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Snare'), 39),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Snare'), 40),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Tom'), 43),
	(SELECT id FROM config_note_cateory WHERE note_category_id = (SELECT id FROM note_category WHERE category = 'Snare'), 47);




CREATE TABLE config_note_format(
	id INTEGER PRIMARY KEY,
	name TEXT,
	chance INTEGER -- True value. False value is 100 minus this value. Likelihood of choosing this format
);
INSERT INTO config_note_format 
	(name, chance)
VALUES
	('All', 0.25),
	('CrashSnare', 0),
	('CrashTom', 0.),
	('HatSnare', 0.1),
	('HatTom', 0.1),
	('HatKickSnareTom', 0.2),
	('HatRide', 0.15),
	('SnareRide', 0.2),




CREATE TABLE config_note_format_definition(
	id INTEGER PRIMARY KEY,
	config_note_format_id INTEGER,
	note_category_id INTEGER,
	chance INTEGER, -- True value. False value is 100 minus this value. Likeliood of a format being selected.
	FOREIGN KEY(note_category_id) REFERENCES note_category(id)
);
INSERT INTO config_note_format_definition 
	(
		config_note_format_id,
		note_category_id,
		chance
	)
VALUES
	((SELECT id FROM config_note_format WHERE name = 'All'), (SELECT id from note_category WHERE category = 'Cymbal Crash'), 5),
	((SELECT id FROM config_note_format WHERE name = 'All'), (SELECT id from note_category WHERE category = 'HiHat'), 15),
	((SELECT id FROM config_note_format WHERE name = 'All'), (SELECT id from note_category WHERE category = 'Kick'), 30),
	((SELECT id FROM config_note_format WHERE name = 'All'), (SELECT id from note_category WHERE category = 'Ride'), 15),
	((SELECT id FROM config_note_format WHERE name = 'All'), (SELECT id from note_category WHERE category = 'Snare'), 20),
	((SELECT id FROM config_note_format WHERE name = 'All'), (SELECT id from note_category WHERE category = 'Tom'), 15),

	((SELECT id FROM config_note_format WHERE name = 'CrashSnare'), (SELECT id from note_category WHERE category = 'Cymbal Crash'), 50),
	((SELECT id FROM config_note_format WHERE name = 'CrashSnare'), (SELECT id from note_category WHERE category = 'Snare'), 50),,

	((SELECT id FROM config_note_format WHERE name = 'CrashTom'), (SELECT id from note_category WHERE category = 'Cymbal Crash'), 50),
	((SELECT id FROM config_note_format WHERE name = 'CrashTom'), (SELECT id from note_category WHERE category = 'Tom'), 50),

	((SELECT id FROM config_note_format WHERE name = 'HatSnare'), (SELECT id from note_category WHERE category = 'HiHat'), 50),
	((SELECT id FROM config_note_format WHERE name = 'HatSnare'), (SELECT id from note_category WHERE category = 'Snare'), 50),

	((SELECT id FROM config_note_format WHERE name = 'HatTom'), (SELECT id from note_category WHERE category = 'HiHat'), 50),
	((SELECT id FROM config_note_format WHERE name = 'HatTom'), (SELECT id from note_category WHERE category = 'Tom'), 50),

	((SELECT id FROM config_note_format WHERE name = 'HatKickSnareTom'), (SELECT id from note_category WHERE category = 'HiHat'), 25),
	((SELECT id FROM config_note_format WHERE name = 'HatKickSnareTom'), (SELECT id from note_category WHERE category = 'Kick'), 25),
	((SELECT id FROM config_note_format WHERE name = 'HatKickSnareTom'), (SELECT id from note_category WHERE category = 'Snare'), 25),
	((SELECT id FROM config_note_format WHERE name = 'HatKickSnareTom'), (SELECT id from note_category WHERE category = 'Tom'), 25),

	((SELECT id FROM config_note_format WHERE name = 'HatRide'), (SELECT id from note_category WHERE category = 'HiHat'), 50),
	((SELECT id FROM config_note_format WHERE name = 'HatRide'), (SELECT id from note_category WHERE category = 'Ride'), 50),

	((SELECT id FROM config_note_format WHERE name = 'RideSnare'), (SELECT id from note_category WHERE category = 'Ride'), 50),
	((SELECT id FROM config_note_format WHERE name = 'RideSnare'), (SELECT id from note_category WHERE category = 'Snare'), 50)




CREATE TABLE config_phrase(
	id INTEGER PRIMARY KEY,
	count_low INTEGER,
	count_high INTEGER,
	record_chance INTEGER, -- True value. False value is 100 minus this value. Likelihood of recording a phrase.
	replay_chance INTEGER-- True value. False value is 100 minus this value. Likelihood of select a phrase to replay.
);
INSERT INTO config_phrase
	(count_low, count_high, record_chance, replay_chance)
VALUES
	(7, 15, 20, 20)




CREATE TABLE config_volume(
	id INTEGER PRIMARY KEY,
	config_session_id INTEGER,
	name TEXT,
	change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing tempo within the current scope.
	scope_change_chance INTEGER, -- True value. False is 100 minus this value. Likelihood of changing the tempo scope.
	FOREIGN KEY(config_session_id) REFERENCES config_session(id)
);
INSERT INTO config_volume
	(config_session_id, change_chance, scope_change_change)
VALUES
	(
		(SELECT id FROM config_session WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_session')),
		(SELECT name FROM default_name WHERE table_name = 'config_volume'), 
		25, 25
	)




CREATE TABLE config_volume_scope(
	id INTEGER PRIMARY KEY,
	config_volume_id INTEGER,
	low INTEGER,
	high INTEGER,
	chance INTEGER,
	FOREIGN KEY(config_volume_id) REFERENCES config_volume(id)	
);
INSERT INTO config_volume_scope
	(config_volume_id, low, high, chance)
VALUES
	((SELECT id FROM config_volume WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_volume')), 0, 32, 10),
	((SELECT id FROM config_volume WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_volume')), 32, 64, 30),
	((SELECT id FROM config_volume WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_volume')), 64, 85, 60),
	((SELECT id FROM config_volume WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_volume')), 86, 96, 20),
	((SELECT id FROM config_volume WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_volume')), 96, 105, 0)
	((SELECT id FROM config_volume WHERE name = (SELECT name FROM default_name WHERE table_name = 'config_volume')), 105, 127, 0)

