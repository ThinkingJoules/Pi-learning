import gspread
import time
import sqlite_lib as sql
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('talk-to-sheets-3d2c8fe70da5.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Test Log').sheet1 #connect to spreadsheet

conn = sqlite_lib.create_connection() #connect to db
#assemble query
time = time.time()
five_mins_ago = int(time) - 300
csTime = sql.last_5_mins(conn,five_mins_ago)

print csTime
#append to spreadsheet

#wks.update_cell(1,1, 'Hello World')
