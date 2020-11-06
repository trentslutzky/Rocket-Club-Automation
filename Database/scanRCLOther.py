import RCData as rcdata
from colorama import Fore, Back, Style
from datetime import datetime
import pgTool as pgtool

launchpad_folder_id = "''"
tech_tuesday_folder_id = "'1eNM_Bio1s1TfXC9iSBZi4UuHtCtSuDAb'"

def parse_score(scoreString):
    scoreSplit = str(scoreString).split()
    score = int(scoreSplit[0])
    return score

def get_sheets(folder_id):
    new_q = folder_id + " in parents "
    results = rcdata.drive_service.files().list(q = new_q,
                                        fields='nextPageToken, files(id,name)',
                                        pageToken=None).execute()
    return results.get('files', [])



def scan_launchpad():
    sheets = get_sheets(launchpad_folder_id)
    data = []
    for sheet in sheets:
        sheet_name = sheet['name']
        sheet_name = sheet_name.replace('  (Responses)','')
        if(sheet_name != 'Unused'):
            current_sheet = rcdata.get_cells(sheet['id'],'A1:1000',sheet_name) 
                # figure out which colum has the member id numbers
            for col in current_sheet[0]:
                if 'Member ID Number' in col:
                    id_index = current_sheet[0].index(col)
                if 'Score' in col:
                    score_index = current_sheet[0].index(col)
                if 'Timestamp' in col:
                    timestamp_index = current_sheet[0].index(col)
            
            sheet_needs_updating = False
            for row in current_sheet:
                if current_sheet.index(row) > 0:
                    new_score = parse_score(row[score_index])
                    member_id = row[id_index]
                    if('#' not in member_id):
                        data.append([int(member_id),new_score])

                        uuid = pgtool.get_member_uuid(member_id)
                        if(uuid != -1):
                            pgtool.add_rf_transaction(int(member_id),'rcl','launchpad',int(new_score))
                            row[id_index] = '#' + row[id_index]
                            sheet_needs_updating = True
                        else:
                            print('[' + Fore.YELLOW + '  warn  ' + Fore.WHITE + ']' + 
                                    ' invalid member id: ' + member_id)
            if sheet_needs_updating:
                rcdata.set_cells(sheet['id'],'A1:1000',current_sheet)

def scan_tech_tuesday():
    sheets = get_sheets(tech_tuesday_folder_id)
    data = []
    for sheet in sheets:
        sheet_name = sheet['name']
        sheet_name = sheet_name.replace('  (Responses)','')
        if(sheet_name != 'Unused'):
            current_sheet = rcdata.get_cells(sheet['id'],'A1:1000',sheet_name) 
                # figure out which colum has the member id numbers
            for col in current_sheet[0]:
                if 'Member ID Number' in col:
                    id_index = current_sheet[0].index(col)
                if 'Score' in col:
                    score_index = current_sheet[0].index(col)
                if 'Timestamp' in col:
                    timestamp_index = current_sheet[0].index(col)
            
            sheet_needs_updating = False
            for row in current_sheet:
                if current_sheet.index(row) > 0:
                    new_score = parse_score(row[score_index])
                    member_id = row[id_index]
                    if('#' not in member_id):
                        data.append([int(member_id),new_score])

                        uuid = pgtool.get_member_uuid(member_id)
                        if(uuid != -1):
                            pgtool.add_rf_transaction(int(member_id),'rcl','tech_tuesday',int(new_score))
                            row[id_index] = '#' + row[id_index]
                            sheet_needs_updating = True
                        else:
                            print('[' + Fore.YELLOW + '  warn  ' + Fore.WHITE + ']' + 
                                    ' invalid member id: ' + member_id)
            if sheet_needs_updating:
                rcdata.set_cells(sheet['id'],'A1:1000',current_sheet)

def main():
    print(Fore.BLUE + 'Updating RCL Tech Tuedsay & Launchpad')
    scan_launchpad()
    scan_tech_tuesday()
if __name__ == '__main__':
    main()











