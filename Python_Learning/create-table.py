import sqlite3
from sqlite3 import Error
import os


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
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
	conn.close
    except Error as e:
        print(e)

def main():

    database = os.getlogin() + '.db'

    sql_create_events_table = """ CREATE TABLE IF NOT EXISTS events (
                                            id integer PRIMARY KEY,
                                            ISO_Week text,
                                            Event_ISO_Date text,
                                            Unix_Time real,
                                            Node text,
                                            Event_Type text,
                                            Duration real
                                        ); """


    conn = create_connection(database)
    create_table(conn, sql_create_events_table)
    return

if __name__ == '__main__':
    main()
