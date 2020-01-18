CREATE TABLE e2i_mapping(
	topic_from varchar(255) NOT NULL PRIMARY KEY,
	topic_to varchar(255) NOT NULL
);

CREATE TABLE i2e_mapping(
	topic_from varchar(255) NOT NULL PRIMARY KEY,
	topic_to varchar(255) NOT NULL
);