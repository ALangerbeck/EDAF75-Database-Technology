from bottle import get, post, run, request, response
import sqlite3
from urllib.parse import unquote

db = sqlite3.connect("theathers.sqlite")

@get('/ping')
def get_ping():
    return("pong")

@post('/reset')
def post_reset():
    c = db.cursor()
    c.executescript(
        """
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
        ('Kino','10'),
        ('Regal','16'),
        ('Skandia','100');

        """
    )
@post('/users/<json_user>')
def post_addUser():
    user = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT 
        INTO customers(username,customer_name,customer_password)
        VALUES (?,?,?)
        RETURNING username
        """,
        [user['username'],user['customer_name'],user['customer_password']]
    )



run(host='localhost', port=3000)