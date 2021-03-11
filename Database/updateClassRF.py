import RCData as rcdata
import pgTool as pgtool
from pgTool import Fore
import sys

master_rf_sheet_id = '1f-kOmd5JvI7p_XQL8xogJ6o3e9TrWq4Un3EupRzu1vA'

def main_alert():
    print(Fore.CYAN + 'Updating Class RF')

def tag():
    print(Fore.WHITE + '[' + Fore.CYAN + 'scanning' + Fore.WHITE + '] scanning RF sheet: ', end='')

def main():
    main_alert()
    master_data = rcdata.get_cells(master_rf_sheet_id,'A3:F1247','Rocket Fuel Master')
    tag()
    for row in master_data:
        member_id = row[0]
        member_uuid = pgtool.get_member_uuid(member_id)
        if(member_uuid != -1):
            current_class_rf = row[5]
            db_class_rf = pgtool.get_member_class_rf(member_uuid)
            if db_class_rf == None:
                db_class_rf = 0
            difference = int(current_class_rf)-db_class_rf
            if difference > 0:
                print(member_id,difference)
                pgtool.add_rf_transaction(member_id,'class','',difference)
if __name__ == ('__main__'):
    main()
