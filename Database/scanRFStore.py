import RCData as rcdata
import pgTool as pgtool
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style

folder_id = "'1UF10kUUytJcOcZRdiULagxzy8BFns7ee'"

def scan_folder(category,folder_id):
    completions = []
    new_q = folder_id + " in parents"
    results = rcdata.drive_service.files().list(q = new_q, 
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=None).execute()
    for sheet in results.get('files', []):
        sheet_name = sheet['name']
        sheet_id = sheet['id']
        if(sheet_name != 'Unused'):
            is_edited = False
            current_sheet = rcdata.get_cells(sheet['id'],'A1:1000',sheet_name)
            id_index = current_sheet[0].index('Member ID')
            rf_index = current_sheet[0].index('Rocket Fuel')
            
            for row in current_sheet:
                if row[id_index] != 'Member ID' and '#' not in row[id_index]:
                    item = sheet_name.replace('RF Store - ','').replace(' Purchase','')
                    member_id = row[id_index]
                    price = int(row[rf_index]) * -1
                    member_total = int(pgtool.get_member_total(member_id))
                    member_uuid = pgtool.get_member_uuid(member_id)

                    if(member_total > (price * -1)):
                        if(member_uuid != -1):
                            pgtool.add_rf_transaction(member_id,'purchase',item,price)
                            row[id_index] = '#' + row[id_index]
                            is_edited = True
                            print(member_id,'bought',item,'for',price)
                        else:
                            print(Fore.WHITE+'['+Fore.YELLOW+'  warn  '+Fore.WHITE+']'+
                                    ' invalid member id: ' + str(member_id))
                    else:
                        print(member_id,'NOT ENOUGH',item,price)

            if is_edited:
                rcdata.set_cells(sheet_id,'A1:1000',current_sheet)

def main():
    print('Scanning RF Store')
    scan_folder('store',folder_id)

if __name__ == "__main__":
    main()
