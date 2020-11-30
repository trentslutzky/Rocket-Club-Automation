# pylint: disable=no-member
# pylint: disable=unused-variable
import RCData as rcdata
import os
import pgTool as pgtool
from pgTool import db
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style
####################################################
import time
from datetime import datetime
########## Trivia Winners Sheet ID ##########
wheel_sheet_id = '1DS1kVaB_WcwY3qCzEbMJjggRSW8NsT4wDMXTnkRovQI'
####################################################

def scan_sheet():
    # get cells from trivia winners sheet
    print(Fore.WHITE+'[ status ] Fetching Winners Sheet')
    wheel_sheet = rcdata.get_cells(wheel_sheet_id, 'A2:G','RCL Wheel Winners')
    # get cells from the master sheet for use later
    print(Fore.WHITE+'[ status ] Scanning Winners Sheet')
    # Calculate how many new entries there are in the sheet
   
    for row in wheel_sheet:
        while(len(row) < 7):
            row.append(' ')

    rows_to_update = 0
    for row in wheel_sheet:
        if((row[6] == 'No' or row[6] == ' ') and row[0] != ''):
            rows_to_update += 1

    # scan each row in sheet and add rocket fuel to master sheet for each winner
    for row in wheel_sheet:
        if((row[6] == 'No' or row[6] == ' ') and row[0] != ''):
            row[6] = 'Yes'
            member_id = row[0]
            prize = row[2]
            # add rf transaction
            pgtool.add_rf_transaction(int(member_id),'wheel_of_names','',int(prize)) 

    if rows_to_update > 0:
        print(Fore.WHITE+'[ status ] Updating wheel sheet - adding "Yes" to updated rows')         
        rcdata.set_cells(wheel_sheet_id,'A2:G',wheel_sheet)
    else:
        print('[ status ] Nothing new!')


def main():
    print(Fore.BLUE + 'Updating Wheel Winners')
    scan_sheet()

if __name__ == '__main__':
    main()
