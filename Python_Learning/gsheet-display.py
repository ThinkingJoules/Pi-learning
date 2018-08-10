#!/usr/bin/python
import gspread
import time
import sqlite_lib
import os
import datetime
from datetime import date
import google_auth
import json
import pytz

gc = google_auth.auth()
node = 'manual-mill'

wks = gc.open('Test Log').worksheet(node)
 #connect to spreadsheet

conn = sqlite_lib.create_connection() #connect to db
#assemble query
currentTime = time.time()
tz = time.altzone
five_mins_ago = int(currentTime) - 300
csTime = sqlite_lib.last_5_mins(conn,five_mins_ago) / 60
if csTime == 0:
	print "don't send to spreadsheet"
	pass
else:
	#now = json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)
	utc_now=pytz.utc.localize(datetime.datetime.utcnow())
	now = utc_now.astimezone(pytz.timezone("America/Denver"))
	dateFormat = str(now.strftime("%m/%d/%y"))
	timeFormat = str(now.strftime("%H:%M:%S"))
	print '{} {} {} {} {}'.format(node,'W' + str(date.today().isocalendar()[1]), 'Cycle Time', csTime,'minutes')
	data = [dateFormat, timeFormat, 'W' + str(date.today().isocalendar()[1]), node, csTime]
        #append to spreadsheet
        wks.append_row(data)
