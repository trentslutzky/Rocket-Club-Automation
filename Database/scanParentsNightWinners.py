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
trivia_sheet_id = '1UpFpPSyJE8qf2Hu5DivCDAJ5V_-01PcUxRBEC5r6oLM'
####################################################

def get_prizes():
    print(Fore.WHITE+'[ status ] Fetching Prizes')
    # get cells from the table within the winners sheet
    prise_table = rcdata.get_cells(trivia_sheet_id, 'J3:K6','Parents Night Winners')
    # store prize values in their own list
    prizes = [prise_table[0][1],prise_table[1][1],prise_table[2][1]]
    #print prize values to console for user confirmation
    print(Fore.WHITE+'[ status ] Prizes:', end=' ')
    print(Fore.YELLOW + 'First: ' + Fore.WHITE + prizes[0], end=' ')
    print(Fore.YELLOW + 'Second: ' + Fore.WHITE + prizes[1], end=' ')
    print(Fore.YELLOW + 'Third: ' + Fore.WHITE + prizes[2])
    #return the prize list for use later.
    return(prizes)

def scan_sheet():
    # get cells from trivia winners sheet
    print(Fore.WHITE+'[ status ] Fetching Winners Sheet')
    trivia_sheet = rcdata.get_cells(trivia_sheet_id, 'B3:H','Parents Night Winners')
    # get prizes for use latee
    prizes = get_prizes()
    # get cells from the master sheet for use later
    print(Fore.WHITE+'[ status ] Scanning Winners Sheet')
    # Calculate how many new entries there are in the sheet
    rows_to_update = 0
    for day in trivia_sheet:
        if(day[6] == 'No' and day[0] != ''):
            rows_to_update += 1
    # scan each row in sheet and add rocket fuel to master sheet for each winner
    for day in trivia_sheet:
        if(day[6] == 'No' and day[0] != ''):
            day[6] = 'Yes'
            for winner in range(6):
                member_id = day[winner]
                place = winner
                place += 1
                if place >= 4:
                    place -= 3
                if place == 1:
                    prize = prizes[0]
                if place == 2:
                    prize = prizes[1]
                if place == 3:
                    prize = prizes[2]
                # add rf transactio
                pgtool.add_rf_transaction(int(member_id),'rcl','parents_night',int(prize)) 
      #          for row in master_data:
      #              if row[0] == day[winner]:
      #                  row[score_col] = str(int(prize) + int(row[score_col]))
        # if new info, update trivia sheet and master sheet with new informations    
    if rows_to_update > 0:
        print(Fore.WHITE+'[ status ] Updating parents night sheet - adding "Yes" to updated rows')                
        rcdata.set_cells(trivia_sheet_id,'B3:H',trivia_sheet)

def main():
    print(Fore.BLUE + 'Updating Parents Night Winners')
    scan_sheet()

if __name__ == '__main__':
    main()
