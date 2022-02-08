DROP TABLE IF EXISTS theater;
CREATE TABLE theater(
    theater_name    TEXT,
    capacity        INT,
    PRIMARY KEY (theater_name)     
);

DROP TABLE if EXISTS screenings;
CREATE TABLE screenings(
    screening_id    TEXT DEFAULT (lower(hex(randomblob(16)))),
    start_date      DATE,
    start_time      TIME,
    theater_name    TEXT,
    imdb_key        TEXT,
    FOREIGN KEY (theater_name) REFERENCES theater(theater_name),
    FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key),
    PRIMARY KEY (start_time,start_date,theater_name)
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies(
    imdb_key        TEXT,
    title           TEXT,
    production_year TEXT,
    running_time    INT,
    PRIMARY KEY (imdb_key)
);

DROP TABLE IF EXISTS tickets;
CREATE TABLE tickets(
    ticket_id       TEXT DEFAULT (lower(hex(randomblob(16)))),
    screening_id    TEXT,
    theater_name    TEXT,
    username        TEXT,
    FOREIGN KEY (screening_id) REFERENCES screenings(screening_id),
    FOREIGN KEY (username) REFERENCES customers(username),
    PRIMARY KEY (ticket_id) 
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers(
    username            TEXT,
    customer_name       TEXT,
    customer_password   TEXT,
    PRIMARY KEY (username)
);


