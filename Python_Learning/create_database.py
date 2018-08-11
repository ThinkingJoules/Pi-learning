import sqlite3
from sqlite3 import Error
import os
nodeName = os.getlogin() + '.db'

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()
    return

if __name__ == '__main__':
    create_connection(nodeName)
