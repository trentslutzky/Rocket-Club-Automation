#########  Needed packages from GOOGLE  ############
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
####################################################
import pg8000, re, secret
import pgTool as pgtool
import RCData as rcdata
import random, string

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

SHEET_ID = '1eOnn_ttpSGAqAlCBAdZPuykrhab0HC4lDyeqcO6lkXU'

def timer(function):
    def rapper():
        start_time = time.time_ns()
        function()
        end_time = time.time_ns()
        time_elapsed = (str(int((end_time-start_time) / 1000000)) + 'ms')
        print(time_elapsed)
    return rapper

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    return db

def qprep(db, string):
    db.run("DEALLOCATE ALL")
    result = db.prepare(string)
    return result

def get_temp_password(email):
    db = connect()
    COMMAND = f"select temp_password from parents where email = '{email}' limit 1;"
    result = db.run(COMMAND)
    db.close()
    if(result):
        return result[0][0]
    else:
        return ''

def get_passwords():
    data = []
    google_data = rcdata.get_cells(SHEET_ID,'A2:E','sheet')
    for row in google_data:
        name = (row[1] + ' ' + row[2])
        temp_password = get_temp_password(row[3])
        try:
            data.append([
                row[0],
                row[1],
                row[2],
                row[3],
                temp_password
                ])
        except:
            print('error in row',row)
    
    rcdata.set_cells(SHEET_ID,'A2:E',data)

def main():
    data = get_passwords()
    print(data)

if __name__ == '__main__':
    main()
