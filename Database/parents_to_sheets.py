#########  Needed packages from GOOGLE  ############
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
####################################################

import pg8000, secret, RCData

SHEET_ID = '1wrMArjaz0gt9cMqRMYdKm4dyMtDk-cPMApNsIlQfYvA'

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

def get_data():
    parents = []
    db = connect()
    ps = "SELECT email,temp_password FROM parents;"
    results = db.run(ps)
    for row in results:
        if row not in parents:
            parents.append(row)
    return parents

def transfer(data):
    range = 'A2:B'
    RCData.set_cells(SHEET_ID,range,data)

def main():
    data = get_data()
    print(data)
    transfer(data)

if __name__ == '__main__':
    main()
