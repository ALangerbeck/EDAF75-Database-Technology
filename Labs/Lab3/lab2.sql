PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theaters;
DROP TABLE if EXISTS screenings;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS customers;

PRAGMA foreign_keys=OFF;

CREATE TABLE theaters(
    theater_name    TEXT,
    capacity        INT,
    PRIMARY KEY (theater_name)     
);

CREATE TABLE screenings(
    screening_id    TEXT DEFAULT (lower(hex(randomblob(16)))),
    starting_date      DATE,
    starting_time      TIME,
    theater_name    TEXT,
    imdb_key        TEXT,
    FOREIGN KEY (theater_name) REFERENCES theaters(theater_name),
    FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key),
    PRIMARY KEY (screening_id)
);

CREATE TABLE movies(
    imdb_key        TEXT,
    title           TEXT,
    production_year INT,
    running_time    INT,
    PRIMARY KEY (imdb_key)
);

CREATE TABLE tickets(
    ticket_id       TEXT DEFAULT (lower(hex(randomblob(16)))),
    screening_id    TEXT,
    username        TEXT,
    FOREIGN KEY (screening_id) REFERENCES screenings(screening_id),
    FOREIGN KEY (username) REFERENCES customers(username),
    PRIMARY KEY (ticket_id) 
);

CREATE TABLE customers(
    username            TEXT,
    customer_name       TEXT,
    customer_password   TEXT,
    PRIMARY KEY (username)
);

INSERT 
INTO theaters(theater_name,capacity)
VALUES  
    ('Filmstaden Martenstorg','300'),
    ('Filmstaden Royal','100'),
    ('Filmstaden Storgatan','50');

INSERT
INTO screenings(starting_date,starting_time,theater_name,imdb_key)
VALUES  ('2022-02-10','18:00','Filmstaden Martenstorg','tt0060196'),
        ('2022-02-11','18:00','Filmstaden Martenstorg','tt0060196'),
        ('2022-02-10','21:00','Filmstaden Martenstorg','tt0482571'),
        ('2022-02-10','18:00','Filmstaden Royal','tt0060196'),
        ('2022-02-10','21:00','Filmstaden Royal','tt0105236'),
        ('2022-02-10','18:00','Filmstaden Storgatan','tt0060196'),
        ('2022-02-10','21:00','Filmstaden Storgatan','tt0108052');

INSERT
INTO movies(imdb_key,title,production_year,running_time)
VALUES  ('tt0060196','The Good, the Bad and the Ugly',1966,178),
        ('tt0482571','The Prestige',2006,130),
        ('tt0105236','Reservoir Dogs',1992,99),
        ('tt0108052','Schindlers List',1993,195);

INSERT
INTO customers(username,customer_name,customer_password)
VALUES  ('Bippi','Bippi Sangstrump','LillaSnubben1337'),
        ('Mippi','Mippi Tangstrump','LillaMubben1337'),
        ('pippi','Pippi Langstrump','LillaGubben1337');

