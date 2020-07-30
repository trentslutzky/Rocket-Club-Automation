# pylint: disable=no-member
#########  Needed packages from GOOGLE  ############
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
####################################################
import time
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style
####################################################

'''
Trent Slutzky
Rocket Club
16 July 2020

This script scans the folder of Virtual Missions Google Forms responses 
and automatically adds rocket fuel to the master sheet.

Requirements:
    Forms/Responses folder organized like the example.
    Master Sheet organized in a specific (simple) way.

TO DO:
    [x] Automate adding Virtual Missions rocket fuel to master sheet
        [ ] Implement weekly totals for use in leaderboards - WORKING ON
    [ ] Instead of hard-coding ranges, use table titles to figure out where data is...
    [x] Implement RC Live Winners
        [ ] Optimize the way the spreadsheet is dealth with 
    [ ] Print to the console the Rocket Fuel leader afeter refreshing

'''
####################  global_variables  ####################
#google drive IDs for crucial items -- IMPORTANT
    #folders
vm_responses_folder_id = '1nGoSFnpwDOTLKjtuw3dzWydFHhVg5LBM'
    #sheets
rc_live_winners_sheet_id = '1PcNbCH5A7oqL0MvKnbGj0FifhDYHTP_r6VwxgJamo6I'
vm_weekly_totals_sheet_id = '16Sx92lCjZMa4H4-zopWDBLkPIpztB6B8dQdCEeUU1fA'
member_stats_sheet_id = '1UkJKMY735oTSohu8X5eM_rvFp267KBbaEiVg4SXaki8'
master_sheet_id = '1hkkeTR4r6Lb8uzqao_0Z2_8k6xrajvtUY4oq2t_Iyk8'
vm_master_sheet_id = '1rVblBZu9FXzM9guC9R5CxQEtYlTN_NGfFiv2X4ivh70'
    #ranges for important sheets:
master_sheet_range = 'A2:F'
rc_live_winners_range = 'B3:H'
rc_live_rewards_range =  'K3:K5'
vm_weekly_totals_range = 'A2:Z'
############################################################

#Authorize Google Drive API with Project
def auth_drive():

    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service
drive_service = auth_drive() # store drive authorization

#Authorize Google Sheets API with Project
def auth_sheets():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service
sheets_service = auth_sheets() # store sheets authorization

sheet = sheets_service.spreadsheets()

base_delay = 0.1
error_delay = 5

def get_cells(sheet_id, newRange):
    while True:
        try:
            result = sheet.values().get(spreadsheetId=sheet_id, range=newRange).execute()
            print(Style.DIM + Fore.WHITE + 'Getting cells', end = '')
            time.sleep(base_delay/4)
            print('.', end = '')
            time.sleep(base_delay/4)
            print('.', end = '')
            time.sleep(base_delay/4)
            print('.', end = ' ')
            time.sleep(base_delay/4)
            values = result.get('values', [])
            if not values:
                print('Range not found.')
                return 
            else:
                print(Style.DIM + Fore.CYAN + 'Got cells for ' + Fore.WHITE + sheet_id + Fore.CYAN + ' on ' + Fore.WHITE + newRange)
                return values
        except:
            print(Fore.RED + '    Quota Hit ' + Fore.WHITE + '- Waiting')
            print('    ', end='')
            time.sleep(error_delay)
        


def set_cells(sheet_id, newRange, values):
    while True:
        try:
            body = {'values': values}
            sheet.values().update(spreadsheetId=sheet_id, 
                                            range=newRange,
                                            valueInputOption='USER_ENTERED',
                                            body=body).execute()
            print(Style.DIM + Fore.WHITE + 'Setting cells', end = '')
            time.sleep(base_delay/4)
            print('.', end = '')
            time.sleep(base_delay/4)
            print('.', end = '')
            time.sleep(base_delay/4)
            print('.', end = ' ')
            time.sleep(base_delay/4)
            print(Style.DIM + Fore.CYAN + 'Set cells for ' + Fore.WHITE + sheet_id + Fore.CYAN + ' on ' + Fore.WHITE + newRange)
            return
        except Exception as error:
            print(str(error))
            print('    ', end='')
            time.sleep(error_delay)
    

def get_member_info(member_stats_data, member_id, stat):
    column = member_stats_data[0].index(stat)
    output = 'null'
    for row in member_stats_data:
        if row[0] == str(member_id):
            output = row[column]
    return output
