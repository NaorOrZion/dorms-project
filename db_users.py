from consts import *
import psycopg2
from flask import g

DB_SCHEMA = f"-c search_path=users-db"
_database = None

def get_db_users():
    """
    The application context in Flask represents a shared environment where
      important resources and variables for the Flask application are stored. 
      It allows different parts of the code to access and share resources like the current request, 
      configuration settings, and database connections. 
      Think of it as a central area in a house where you can find and use things that are shared among different rooms. 
      The application context ensures efficient communication and resource management within the Flask application so you won't
      have to pass data(by parameters) to functions every time.

    The "g" object in Flask is part of the application context. It's a special space where you
      can temporarily store information during the handling of a single request.
      It's like a little notebook that you can use to keep track of important data,
      and it gets automatically cleared out when the request is done.
    """
    global _database
    try:
        # try to use Flask's g object to store and retrieve the database connection
        db = getattr(g, "_database", None)
    except RuntimeError:
        # if there is no Flask application context available, use a global variable instead
        db = _database

    if db is None:
        db = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            options=DB_SCHEMA
        )
        try:
            # try to store the database connection in Flask's g object
            g._database = db
        except RuntimeError:
            # if there is no Flask application context available, store it in a global variable instead
            _database = db

    return db

def close_connection(exception):
    try:
        # try to retrieve the database connection from Flask's g object
        db = getattr(g, "_database", None)
    except RuntimeError:
        # if there is no Flask application context available, retrieve it from a global variable instead
        db = _database

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)
