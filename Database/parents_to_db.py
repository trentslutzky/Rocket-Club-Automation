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

SHEET_ID = '1ErBowZUj8WTb7NHMLD4cFisHM03GAMuWoeVtyCywGTI'

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

def clean_name(name):
    name_output = ''
    # remove double spaces
    name_output = name.replace("  "," ")
    return name_output

def generate_username_from_name(name):
    username = name.replace(' ','')
    rx = re.compile('\W+')
    username = rx.sub('',username).strip()
    return username

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def get_data():
    data = []
    google_data = rcdata.get_cells(SHEET_ID,'A2:F','sheet')
    for row in google_data:
        random_password = get_random_alphanumeric_string(10)
        pw_hash = bcrypt.generate_password_hash(random_password).decode('utf-8')
        print(row[0],random_password,pw_hash)
        data.append({
            'name':row[0],
            'email':row[1],
            'phone':row[2],
            'assoc_member':pgtool.get_member_uuid(row[3]),
            'tuition':row[4],
            'scholarship':row[5],
            'username':generate_username_from_name(row[0]),
            'temp_password':random_password,
            'pw_hash':pw_hash
            })
    return data

def add_users_to_db(users):
    db = connect()
    for user in users:
        command = f"INSERT INTO parents(name,username,email,pw_hash,\
phone,assoc_member,tuition,scholarship,temp_password) VALUES(\
'{user['name']}',\
'{user['username']}',\
'{user['email']}',\
'{user['pw_hash']}',\
'{user['phone']}',\
'{user['assoc_member']}',\
{user['tuition']},\
{user['scholarship']},\
'{user['temp_password']}')"
        print(command)
        db.run(command)
        db.commit()
    db.close()

def main():
    data = get_data()
    add_users_to_db(data)

if __name__ == '__main__':
    main()
