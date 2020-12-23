# pylint: disable=no-member
# pylint: disable=unused-variable
import RCData as rcdata
import pgTool as pgtool
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style

########### Virtual Missions Folder IDs ############
ent_1_folder_id = "'1tJWNQnqWLPUw7zZwJ6_ZHW74xBw04K7_'"

def parse_score(scoreString):
    scoreSplit = str(scoreString).split()
    score = int(scoreSplit[0])
    return score

def scan_folder(category,folder_id):
    completions = []
    new_q = folder_id + " in parents"
    results = rcdata.drive_service.files().list(q = new_q, 
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=None).execute()
    for sheet in results.get('files', []):
        sheet_id = sheet['id']
        sheet_name = sheet['name']
        sheet_name = sheet_name.replace('  (Responses)','')
        sheet_name = sheet_name.replace(' (Responses)','')
        if(sheet_name != 'Unused'):
            is_edited = False
            current_sheet = rcdata.get_cells(sheet['id'],'A1:1000',sheet_name)
            try:
                id_index = current_sheet[0].index('Member ID Number ')
            except:
                id_index = current_sheet[0].index('Member ID Number')
            score_index = current_sheet[0].index('Score')
            for row in current_sheet:
                if row[score_index] != 'Score' and '#' not in row[id_index]:
                    is_edited = True
                    bad_chars = [' ','#']
                    member_id = row[id_index]
                    for i in bad_chars:
                        clean_id = member_id.replace(i,'')
                    try:
                        clean_id = int(clean_id)
                    except:
                        clean_id = 0
                    score = parse_score(str(row[score_index]))
                    member_uuid = pgtool.get_member_uuid(clean_id)
                    vm_tag = pgtool.get_vm_tag(sheet_id)

                    if(member_uuid != -1):
                        pgtool.add_rf_transaction(clean_id,'virtual_mission',str(category),score)
                    else:
                        print(Fore.WHITE+'['+Fore.YELLOW+'  warn  '+Fore.WHITE+']'+
                                ' invalid member id: ' + str(member_id))
                    row[id_index] = '#' + row[id_index]
            if is_edited:
                rcdata.set_cells(sheet_id,'A1:1000',current_sheet)


def get_sheet_ids(category,folder_id):
    completions = []
    new_q = folder_id + " in parents"
    results = rcdata.drive_service.files().list(q = new_q, 
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=None).execute()
    for sheet in results.get('files', []):
        sheet_id = sheet['id']
        sheet_name = sheet['name']
        print(sheet_id + ' ' + sheet_name)


def main():
    print(Fore.BLUE + 'Updating Virtual Missions' + Fore.BLUE)
    scan_folder('ent_1',ent_1_folder_id)

if __name__ == '__main__':
    main()

























