# pylint: disable=no-member
# pylint: disable=import-error
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style
####################################################

import RCData as rcdata
import scanTriviaWinners
import scanVirtualMissions
import scanRCLAttendance
import scanParentsNight
import injectFormulas
from datetime import datetime
import os

def do_total_column():
    print(Fore.GREEN + 'Calculating Totals -> ',end = '')
    master_sheet = rcdata.get_cells(rcdata.master_sheet_id, 'A2:1000')
    total_column_num = master_sheet[0].index('total_rf')
    for row in master_sheet:
        r = str(master_sheet.index(row)+2)
        formula = '=SUM(E' + r + ':P' + r + ')'
        if(int(r) > 2):
            row[total_column_num] = formula
    print(Fore.GREEN + 'Refreshing Totals Column -> ',end = '')
    rcdata.set_cells(rcdata.master_sheet_id,'A2:1000',master_sheet)

def main():
    start_time = datetime.now()
    os.system('clear')
    scanTriviaWinners.main()
    scanRCLAttendance.main()
    scanParentsNight.main()
    scanVirtualMissions.main()
    injectFormulas.main()
    final_time = datetime.now()
    time_difference = final_time - start_time
    print(Fore.YELLOW + 'Finished in ' + Fore.WHITE + str(time_difference))


if __name__ == '__main__':
    main()
