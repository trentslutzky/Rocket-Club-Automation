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
purchases_sheet_id = '1seSiLrJFxD-oz5pEIFIV7BekLnNLTrbKLZTRfZjWcMA'
purchases_sheet_range = 'A3:D'
####################################################

def scan_sheet():
    # get cells from trivia winners sheet
    print(Fore.WHITE+'[ status ] Fetching Purchases Sheet')
    purchases_sheet = rcdata.get_cells(purchases_sheet_id, purchases_sheet_range,'Purchases')
    # get cells from the master sheet for use later
    print(Fore.WHITE+'[ status ] Scanning Purchases Sheet')
    # Calculate how many new entries there are in the sheet
        
    # Boolean for whether or not sheet needs to be updated
    need_to_update = False

    for row in purchases_sheet:
        if '#' not in row[3]:
            member_id = row[1]
            price = row[3]
            purchase = row[2]
            print('[ status ]',member_id,'bought',purchase[:15],'for',price,'RF')
        # add rf transactio
        #pgtool.add_rf_transaction(int(member_id),'rcl','trivia',int(prize)) 
      #          for row in master_data:
      #              if row[0] == day[winner]:
      #                  row[score_col] = str(int(prize) + int(row[score_col]))
        # if new info, update trivia sheet and master sheet with new informations    
    if need_to_update == True:
        print(Fore.WHITE+'[ status ] Updating purchases sheet...')                
        #rcdata.set_cells(trivia_sheet_id,'B3:H',trivia_sheet)

def main():
    print(Fore.BLUE + 'Updating Purchases')
    scan_sheet()

if __name__ == '__main__':
    main()
