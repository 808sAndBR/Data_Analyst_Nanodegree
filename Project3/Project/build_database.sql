CREATE TABLE node
(
	id INTEGER PRIMARY KEY NOT NULL,
	lat REAL,
	lon REAL,
	user TEXT,
	uid INTEGER,
	version INTEGER,
	changeset INTEGER,
	timestamp TEXT
);

CREATE TABLE node_tags
(
	id INTEGER,
	key TEXT,
	value TEXT,
	type TEXT,
	FOREIGN KEY (id) REFERENCES nodes(id)
);

CREATE TABLE way
(
	id INTEGER PRIMARY KEY NOT NULL,
	user TEXT,
	uid INTEGER,
	version TEXT,
	changeset INTEGER,
	timestamp TEXT
);

CREATE TABLE way_nodes
(
	id INTEGER NOT NULL,
	node_id INTEGER NOT NULL,
	position INTEGER NOT NULL,
	FOREIGN KEY (id) REFERENCES ways(id),
    FOREIGN KEY (node_id) REFERENCES nodes(id)
);

CREATE TABLE way_tags
(
	id INTEGER NOT NULL,
	key TEXT NOT NULL,
	value TEXT NOT NULL,
	type TEXT,
	FOREIGN KEY (id) REFERENCES ways(id)
);

.mode csv
.import processed_data/nodes.csv node
.import processed_data/nodes_tags.csv node_tags
.import processed_data/ways.csv way
.import processed_data/ways_nodes.csv way_nodes
.import processed_data/ways_tags.csv way_tags