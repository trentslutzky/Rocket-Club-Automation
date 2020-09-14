import RCData as rcdata
import pgTool as pgt
from pgTool import Fore
import sys

master_rf_sheet_id = '1hkkeTR4r6Lb8uzqao_0Z2_8k6xrajvtUY4oq2t_Iyk8'

def main_alert():
    print(pgt.Fore.CYAN + 'Updating Class RF')

def tag():
    print(Fore.WHITE + '[' + Fore.CYAN + 'scanning' + Fore.WHITE + '] scanning RF sheet: ', end='')

def main():
    main_alert()
    master_data = rcdata.get_cells(master_rf_sheet_id,'A3:K')
    tag()
    for row in master_data:
        member_id = row[0]
        current_class_rf = row[10]
        db_class_rf = pgt.get_member_class_rf(member_id)
      
        if(db_class_rf is not None):
            rf_difference = int(current_class_rf) - int(db_class_rf)
        else:
            rf_difference = None

        if(rf_difference is not None):
            if(rf_difference > 0):
                print(Fore.YELLOW, end='')
            else:
                print(Fore.GREEN, end='')
        else:
            print(Fore.RED, end='')

        print(str(member_id), end = '  ')
        print(pgt.Fore.WHITE + str(rf_difference))
        tag()
        if(rf_difference is not None):
            if(rf_difference > 0):
                pgt.add_rf_transaction(member_id,'class','',rf_difference)
    print('done           ')

if __name__ == ('__main__'):
    main()
