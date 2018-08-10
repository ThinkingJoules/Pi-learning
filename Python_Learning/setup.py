import os
import gspread
import google_auth
import create_database
import create_table


"""
Prerequisites:
-Change user name to match node (what machine it is tracking)
-pip must be installed
-install gspread using pip
-ran setup.py for gspread
-created a google api key and loaded the json file on pi
-updated googleauth.py with json file name
-created a spreadsheet and share it with api email

This file will:
-create the local db and tables
-create a sheet on the google sheet for this node

You will still need to:
-add gsheet-display to cron every 5 min
-add [weekly summary dump] to cron every mon at 5am
-add [weekly backup db dump] to cron every sun at 8p

"""
#Create Google Stuff
gc = google_auth.auth()
node = os.getlogin()
print 'Creating new worksheet!'
create = gc.add_worksheet(title=node, rows="2", cols="10") #create sheet
wks = gc.open('Test Log').worksheet(node) #select create sheet
print 'Adding header to new sheet!'
header = ['Timestamp','ISO Week','Machine','Cycle Start Time (mins)']
wks.update_cells(header) #add header

#create database
print 'Now for some database fun! Lets create one!'
create_database.main()
print 'Hold your hats! Here comes a table!'
create_table.main()
print 'fin'
