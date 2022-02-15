from http.client import FOUND
from turtle import title
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
    print("Resetting Database")
    c.executescript(
        """
        PRAGMA foreign_keys=OFF;

        DROP TABLE IF EXISTS theaters;
        DROP TABLE if EXISTS screenings;
        DROP TABLE IF EXISTS movies;
        DROP TABLE IF EXISTS tickets;
        DROP TABLE IF EXISTS customers;

        PRAGMA foreign_keys=ON;

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
    print("Database Reset")

@post('/users')
def post_addUser():
    user = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT 
            INTO customers(username,customer_name,customer_password)
            VALUES (?,?,?)
            RETURNING username
            """,
            [user['username'],user['fullName'],user['pwd']]
        )
        found = c.fetchone()
        if not found:
            response.status = 500
            return "Something went wrong"
            print("shit")
        else:
            response.status = 201
            username, = found
            return f"http://localhost:3000/users/{username}"
    except sqlite3.IntegrityError:
        response.status = 400
        return ""

@post('/movies')
def post_addUser():
    movie = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT 
            INTO movies(imdb_key,title,production_year)
            VALUES (?,?,?)
            RETURNING imdb_key
            """,
            [movie['imdbKey'],movie['title'],movie['year']]
        )
        found = c.fetchone()
        if not found:
            response.status = 500
            return "Something went wrong"
            print("shit")
        else:
            response.status = 201
            imdbKey, = found
            return f"http://localhost:3000/users/{imdbKey}"
    except sqlite3.IntegrityError:
        response.status = 400
        return ""

@get('/movies')
def get_movies():
    query = """
        SELECT   imdb_key, title, production_year
        FROM     movies
        WHERE    1 = 1
        """
    params = []
    if request.query.title:
        query += " AND title = ?"
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND production_year = ?"
        params.append(request.query.year)
    c = db.cursor()
    c.execute(query,params)
    found = [{"imdbKey": imdb_key, "title": title, "year": production_year}
         for imdb_key, title, production_year in c]
    response.status = 200
    return {"data": found}

@get('/movies/<imdbKey>')
def get_movies(imdbKey):
    c = db.cursor()
    c.execute(
        """
        SELECT imdb_key, title,production_year
        FROM movies
        Where imdb_key = ?
        """,
        [imdbKey]
    )
    found = [{"imdbKey":imdb_key, "title":title,"year":production_year}
        for imdb_key,title,production_year in c]
    response.status = 200
    return{"data":found}


@post('/performances')
def post_addUser():
    screening = request.json
    c = db.cursor()
    try:
        c.execute(
            """
            INSERT 
            INTO screenings(imdb_key,theater_name, starting_date, starting_time)
            VALUES (?,?,?,?)
            RETURNING screening_id
            """,
            [screening['imdbKey'],screening['theater'],screening['date'],screening['time']]
        )
        found = c.fetchone()
        if not found:
            response.status = 500
            return "Something went wrong"
            print("shit")
        else:
            response.status = 201
            screening_id, = found
            return f"http://localhost:3000/performances/{screening_id}"
    except sqlite3.IntegrityError:
        response.status = 400
        return "No such movie or theater"

run(host='localhost', port=3000)