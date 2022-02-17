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
            return f"/users/{username}"
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
            return f"/movies/{imdbKey}"
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
            return f"/performances/{screening_id}"
    except sqlite3.IntegrityError:
        response.status = 400
        return "No such movie or theater"
    db.commit()


@get('/performances')
def get_performances():
    query = """
        SELECT   screening_id, starting_date, starting_time, title, production_year, theater_name
        FROM     movies
        JOIN screenings 
        USING (imdb_key)
        JOIN theaters 
        USING (theater_name)
        """
    c = db.cursor()
    c.execute(query)
    
    found = []
    for row in c:
        screening_id = row[0]
        starting_date = row[1]
        starting_time = row[2]
        title = row[3]
        production_year = row[4]
        theater_name = row[5]
        c2 = db.cursor()
        c2.execute(
            """
            SELECT capacity
            FROM theaters
            WHERE theater_name = ?
            """, [theater_name]
            )
        capacity = c2.fetchone()[0]
        c2.execute(
            """
            SELECT count(screening_id)
            FROM tickets
            WHERE screening_id = ?

            """,[screening_id]
            )
        no_tickets = c2.fetchone()[0]
        d = dict()
        d['performanceId'] = screening_id
        d['date'] = starting_date
        d['startTime'] = starting_time
        d['title'] = title
        d['year'] = production_year
        d['theater'] = theater_name
        d['remainingSeats'] = (capacity - no_tickets)
        found.append(d)

    response.status = 200
    return {"data": found}

@post('/tickets')
def post_tickets():
    try :
        ticket = request.json
        c2 = db.cursor()
        c2.execute(
            """
            SELECT capacity,screening_id
            FROM screenings
            JOIN  theaters
            USING (theater_name)
            WHERE screening_id = ?
            """, [ticket["performanceId"]]
            )
        capacity = c2.fetchone()[0]

        c2.execute(
            """
            SELECT count(screening_id)
            FROM tickets
            WHERE screening_id = ?

            """,[ticket["performanceId"]]
            )
        no_tickets = c2.fetchone()[0]

        if ((capacity - no_tickets)  == 0):
            response.status = 400
            return "No tickets left"
        c2.execute(
            """
            SELECT username
            FROM customers
            WHERE username = ? AND customer_password = ?
            """,[ticket["username"],ticket["pwd"]]
            )
        if c2.fetchone()[0] == None:
            response.status = 401
            return "Wrong user credentials"
        c2.execute(
            """
            INSERT INTO tickets(screening_id,username)
            VALUES (?,?)
            RETURNING ticket_id
            """,[ticket["performanceId"],ticket["username"]]
            )
        ticket_id = c2.fetchone()[0]
        response.status = 201
        return f"/tickets/{ticket_id}"
    
    except sqlite3.IntegrityError:
        response.status = 400
        return "Error"


@get('/users/<username>/tickets')
def getTickets(username):
    c2 = db.cursor()
    c2.execute(
        """
        WITH nbr_ticket(screening_id, nbr_tickets) AS (
            SELECT screening_id,count() AS nbr_tickets
            FROM tickets
            WHERE username = ?
            GROUP BY screening_id )
        SELECT starting_date,starting_time,theater_name,title,production_year,nbr_tickets
        FROM screenings
        JOIN movies
        USING (imdb_key)
        JOIN nbr_ticket
        USING (screening_id)
        """,[username]
        )

    found = [{"date":starting_date, "startTime":starting_time,"theater":theater_name,"title":title,"year":production_year,"nbrOfTickets":nbr_tickets}
        for starting_date,starting_time,theater_name,title,production_year,nbr_tickets in c2]
    response.status = 201
    return {"data": found}



run(host='localhost', port=7007)