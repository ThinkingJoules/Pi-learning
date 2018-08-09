import sqlite3
from sqlite3 import Error
import os


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        database = os.getlogin() + '.db'
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
	conn.commit()
    except Error as e:
        print(e)

def create_event(conn, event):
    """
    Create a new project into the projects table
    :param conn:
    :param create_record:
    :return: events id
    """
    sql = ''' INSERT INTO events(ISO_Week,Event_ISO_Date,Unix_Time,Node,Event_Type,Duration)
              VALUES(?,?,?,?,?,?) '''
    c = conn.cursor()
    c.execute(sql, event)
    conn.commit()
    return c.lastrowid

def last_5_mins(conn,from_time):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param time, now:
    :return:
    """
    c = conn.cursor()
    c.execute("SELECT sum(Duration)"
                "FROM events"
                "[WHERE Unix_Time > ?;",from_time)

    durTot = round(cur.fetchone(),2)
    return durTot
