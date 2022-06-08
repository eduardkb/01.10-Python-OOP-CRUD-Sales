import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


if __name__ == '__main__':
    conn = create_connection(".\dbTest\pythonsqlite.db")
    sSql = """CREATE TABLE IF NOT EXISTS clients (
	            id integer PRIMARY KEY,
	            name text NOT NULL);"""

    # execute sql
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sSql)
        except Exception as e:
            print(e)
