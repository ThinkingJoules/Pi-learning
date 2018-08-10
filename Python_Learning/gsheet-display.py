#!/usr/bin/python
import gspread
import time
import sqlite_lib
import os
import datetime
from datetime import date
import google_auth
import json

gc = google_auth.auth()
node = 'manual-mill'

wks = gc.open('Test Log').worksheet(node)
 #connect to spreadsheet

conn = sqlite_lib.create_connection() #connect to db
#assemble query
time = time.time()
five_mins_ago = int(time) - 300
csTime = sqlite_lib.last_5_mins(conn,five_mins_ago) / 60
if csTime == 0:
	print "don't send to spreadsheet"
	pass
else:
	now = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
	print '{} {} {} {} {}'.format(node,'W' + str(date.today().isocalendar()[1]), 'Cycle Time', csTime,'minutes')
	data = [now,'W' + str(date.today().isocalendar()[1]), node, csTime]
        #append to spreadsheet
        wks.append_row(data)
