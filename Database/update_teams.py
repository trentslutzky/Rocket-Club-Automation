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

SHEET_ID = '14zhPnbKVmwLqRKLTAa7DTIZLhTTaCpPyHKPLwv8minM'

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
    data = []
    google_data = rcdata.get_cells(SHEET_ID,'A2:D','teams')
    for row in google_data:
        data.append({
            'team_name':row[0],
            'instructor':row[1],
            'day':row[2],
            'time':row[3],
            })
    return data

def set_instructor(team_name,instructor):
    db = connect()  
    command = f"UPDATE teams SET instructor='{instructor}' WHERE team_name='{team_name}'"
    db.run(command)
    db.commit()
    db.close()

def set_day(team_name,day):
    db = connect()  
    command = f"UPDATE teams SET day='{day}' WHERE team_name='{team_name}'"
    db.run(command)
    db.commit()
    db.close()

def set_time(team_name,time):
    db = connect()  
    command = f"UPDATE teams SET time='{time}' WHERE team_name='{team_name}'"
    db.run(command)
    db.commit()
    db.close()

def upate_teams(teams):
    db = connect()
    for team in teams: 
        team_name = team['team_name']
        instructor = team['instructor']
        day = team['day']
        time = team['time']
        test = qprep(db,f"select count(*) from teams where team_name = '{team_name}'")
        is_in = test.run()[0][0]
        if(is_in):
            get_team = qprep(db,f"select instructor,day,time from teams where team_name='{team_name}'")
            old_team = get_team.run()[0]
            old_team_instructor = old_team[0]
            old_team_day = old_team[1]
            old_team_time = old_team[2]
            if(old_team_instructor != instructor):
                print(instructor)
                set_instructor(team_name,instructor)
            if(old_team_day != day):
                print(day)
                set_day(team_name,day)
            if(old_team_time != time):
                print(time)
                set_time(team_name,time)

def main():
    data = get_data()
    upate_teams(data)

if __name__ == '__main__':
    main()
