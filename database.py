import sqlite3

DB_PATH = "social_mediaDB.db"

def get_db_connection():
    #Creates and returns a new DB connection 
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn