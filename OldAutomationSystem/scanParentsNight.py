# pylint: disable=no-member
# pylint: disable=unused-variable
import RCData as rcdata
import os
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style
####################################################
import time
from datetime import datetime
########## Parents Night Winners Sheet ID ##########
pn_sheet_id = '1UpFpPSyJE8qf2Hu5DivCDAJ5V_-01PcUxRBEC5r6oLM'
####################################################

def get_prizes():
    print(Fore.GREEN + 'Fetching Prizes -> ', end = ' ')
        # get cells from the table within the winners sheet
    prise_table = rcdata.get_cells(pn_sheet_id, 'J3:K6')
        # store prize values in their own list
    prizes = [prise_table[0][1],prise_table[1][1],prise_table[2][1]]
        #print prize values to console for user confirmation
    print(Fore.BLUE + 'Prizes:', end=' ')
    print(Fore.YELLOW + 'First: ' + Fore.WHITE + prizes[0], end=' ')
    print(Fore.YELLOW + 'Second: ' + Fore.WHITE + prizes[1], end=' ')
    print(Fore.YELLOW + 'Third: ' + Fore.WHITE + prizes[2])
        #return the prize list for use later.
    return(prizes)

def scan_sheet():
        # get cells from pn winners sheet
    print(Fore.GREEN + 'Fetching Winners Sheet -> ', end = ' ')
    pn_sheet = rcdata.get_cells(pn_sheet_id, 'B3:H')
        # get prizes for use latee
    prizes = get_prizes()
        # get cells from the master sheet for use later
    print(Fore.GREEN + 'Fetching master sheet -> ', end = ' ')
    master_data = rcdata.get_cells(rcdata.master_sheet_id,'A2:1000')
    score_col = master_data[0].index('rc_live_pn')
    print(Fore.GREEN + 'Scanning Winners Sheet')
        # Calculate how many new entries there are in the sheet
    rows_to_update = 0
    for day in pn_sheet:
        if(day[6] == 'No' and day[0] != ''):
            rows_to_update += 1
    print(Fore.WHITE + '    New Entries: ' + Fore.BLUE + str(rows_to_update))
        # scan each row in sheet and add rocket fuel to master sheet for each winner
    for day in pn_sheet:
        if(day[6] == 'No' and day[0] != ''):
            day[6] = 'Yes'
            for winner in range(6):
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
                # add rf to master sheet:
                for row in master_data:
                    if row[0] == day[winner]:
                        row[score_col] = str(int(prize) + int(row[score_col]))
        # if new info, update pn sheet and master sheet with new informations    
    if rows_to_update > 0:
        print(Fore.GREEN + 'Updating pn sheet -> ', end = ' ')                
        rcdata.set_cells(pn_sheet_id,'B3:H',pn_sheet)
        print(Fore.GREEN + 'Updating master sheet -> ', end = ' ')
        rcdata.set_cells(rcdata.master_sheet_id,'A2:1000',master_data)
    return

def main():
    print(Fore.BLUE + '############################################')
    print(Fore.BLUE + '####   Updating Parents Night Winners   ####')
    print(Fore.BLUE + '############################################')
    scan_sheet()

if __name__ == '__main__':
    main()
