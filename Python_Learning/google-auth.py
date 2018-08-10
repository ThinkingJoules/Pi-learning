import gspread
from oauth2client.service_account import ServiceAccountCredentials


def auth ()
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('talk-to-sheets-3d2c8fe70da5.json', scope)

    gc = gspread.authorize(credentials)

    return gc
