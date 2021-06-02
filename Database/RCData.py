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

####################  global_variables  ####################
#google drive IDs for crucial items -- IMPORTANT
    #folders
master_sheet_id = '1hkkeTR4r6Lb8uzqao_0Z2_8k6xrajvtUY4oq2t_Iyk8'
vm_responses_folder_id = '1nGoSFnpwDOTLKjtuw3dzWydFHhVg5LBM'
    #sheets
rc_live_winners_sheet_id = '1PcNbCH5A7oqL0MvKnbGj0FifhDYHTP_r6VwxgJamo6I'
vm_weekly_totals_sheet_id = '16Sx92lCjZMa4H4-zopWDBLkPIpztB6B8dQdCEeUU1fA'
member_stats_sheet_id = '1UkJKMY735oTSohu8X5eM_rvFp267KBbaEiVg4SXaki8'
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

base_delay = 1
base_delay_site = .1
error_delay = 5

def scan_folder(folder_id):
    new_q = folder_id + " in parents"
    children = drive_service.files().list(q = new_q, 
                                    fields='nextPageToken, files(id, name,trashed,mimeType)',
                                    pageToken=None).execute() 
    result = []
    for child in children.get('files',[]):
        # only get files that are spreadsheets and not in the trash
        if child['trashed'] == False:
            if child['mimeType'] == 'application/vnd.google-apps.spreadsheet':
                result.append(child)
    return result

def rename_sheet(sheet_id,name):
    drive_service.files().update(fileId=sheet_id,body={'name':name}).execute()

def get_cells(sheet_id, newRange, sheet_name):
    while True:
        try:
            result = sheet.values().get(spreadsheetId=sheet_id, range=newRange).execute()
            print(Fore.WHITE + '[' + Fore.GREEN + ' google ' + Fore.WHITE+']', end = '')
            time.sleep(base_delay)
            values = result.get('values', [])
            if not values:
                print('Range not found.')
                return 
            else:
                print(Fore.CYAN + ' GET ' + Fore.WHITE + sheet_id[:6] + ' "' + Fore.CYAN 
                        + sheet_name[-25:] + Fore.WHITE + '"')
                return values
        except Exception as error:
            print(Fore.WHITE+'['+Fore.RED+' error  '+Fore.WHITE+']',end=' ')
            if 'requests' in str(error):
                print('read request quota hit')
            else:
                print(str(error))
            time.sleep(error_delay)

def set_cells(sheet_id, newRange, values):
    while True:
        try:
            body = {'values': values}
            sheet.values().update(spreadsheetId=sheet_id, 
                                            range=newRange,
                                            valueInputOption='USER_ENTERED',
                                            body=body).execute()
            print(Fore.WHITE+'['+Fore.GREEN+' google '+Fore.WHITE+']', end = '')
            time.sleep(base_delay)
            print(Fore.YELLOW + ' SET ' + Fore.WHITE + sheet_id[:10] + '... ' 
                    + Fore.CYAN + ' on ' + Fore.WHITE + newRange)
            return
        except Exception as error:
            print(Fore.WHITE+'['+Fore.RED+' error  '+Fore.WHITE+']',end=' ')
            if 'requests' in str(error):
                print('read request quota hit')
            else:
                print(str(error))
            time.sleep(error_delay)
    
def get_member_info(member_stats_data, member_id, stat):
    column = member_stats_data[0].index(stat)
    output = 'null'
    for row in member_stats_data:
        print(row[0])
        if str(row[0]) == str(member_id):
            output = row[column]
    return output
