import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('talk-to-sheets-3d2c8fe70da5.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open('Test Log').sheet1

wks.update_cell(1,1, 'Hello World')