import sqlite3
import os
from sqlite3 import Error

nodeName = os.getlogin() + '.db'

conn = sqlite3.connect(str(nodeName))
cursor = conn.cursor()


sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS Events (
                                        id integer PRIMARY KEY,
                                        ISO_Week text,
                                        Event_ISO_Date text,
                                        Unix_Time real,
                                        Event_Type text
                                        Duration real,
                                    ); """

conn.close()
