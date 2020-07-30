# pylint: disable=no-member
# pylint: disable=unused-variable
import RCData as rcdata
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style
########### Virtual Missions Folder IDs ############
coding_vm_folder_id = "'1SG63RmmC42yQ_eR_-dq9IPfWC83DsRbg'"
########## Virtual Missions Main Sheet ID ##########
vm_master_sheet_id = '1rVblBZu9FXzM9guC9R5CxQEtYlTN_NGfFiv2X4ivh70'
####################################################

def parse_score(scoreString):
    scoreSplit = str(scoreString).split()
    score = int(scoreSplit[0])
    return score

def scan_folder(keyword,folder_id):
    print(Fore.BLUE + 'Scanning ' + Fore.GREEN + keyword)
    print(Fore.GREEN + 'Fetch master VM sheet -> ', end = ' ')
    vm_master_data = rcdata.get_cells(vm_master_sheet_id,'A2:1000')
    score_col = vm_master_data[0].index(keyword)
    id_col = vm_master_data[0].index('member_id')
    new_q = folder_id + " in parents"
    scores_updated = 0
    results = rcdata.drive_service.files().list(q = new_q, 
                                    fields='nextPageToken, files(id, name)',
                                    pageToken=None).execute()
    scans = 0
    for sheet in results.get('files', []):
        sheet_id = sheet['id']
        sheet_name = sheet['name']
        if(sheet_name != 'Unused'):
            scans += 1
            print(Fore.BLUE + str(scans) + Fore.WHITE + ' - Scanning ' + Fore.GREEN + sheet_name[:40] + '...')
            print('    ', end='')
            current_sheet = rcdata.get_cells(sheet['id'],'A1:1000')
            id_index = current_sheet[0].index('Member ID Number ')
            score_index = current_sheet[0].index('Score')
            sheet_needs_updating = False
            for row in current_sheet:
                if row[score_index] != 'Score':
                    member_id = row[id_index]
                    if('#' not in member_id):
                        sheet_needs_updating = True
                        score = parse_score(str(row[score_index]))
                        print('    ' + Fore.YELLOW + member_id + Fore.WHITE + ' got ' + Fore.YELLOW + str(score))
                        for master_row in vm_master_data:
                            if master_row[id_col] == member_id:
                                master_row[score_col] = str(int(master_row[score_col]) + score)
                        row[id_index] = '#' + row[id_index]
            if sheet_needs_updating:
                print(Fore.WHITE + '    Updating sheet -> ', end = ' ')
                rcdata.set_cells(sheet['id'],'A1:1000',current_sheet)
            else:
                print(Fore.WHITE + '    No new data.')
    print(Fore.BLUE + 'Finished Scanning ' + Fore.GREEN + keyword + '!')
    print(Fore.GREEN + 'Updating Master Sheet -> ',end = '')
    rcdata.set_cells(vm_master_sheet_id,'A2:1000',vm_master_data)

def do_total_column():
    print(Fore.GREEN + 'Calculating Totals -> ',end = '')
    vm_master_sheet = rcdata.get_cells(vm_master_sheet_id, 'A2:1000')
    total_column_num = vm_master_sheet[0].index('vm_total')
    for row in vm_master_sheet:
        r = str(vm_master_sheet.index(row)+2)
        formula = '=SUM(D' + r + ':' + r + ')'
        if(int(r) > 2):
            row[total_column_num] = formula
    print(Fore.GREEN + 'Refreshing Totals Column -> ',end = '')
    rcdata.set_cells(vm_master_sheet_id,'A2:1000',vm_master_sheet)

def main():
    print(Fore.BLUE + '#####################################')
    print(Fore.BLUE + '###   Updating Virtual Missions   ###')
    print(Fore.BLUE + '#####################################')
    scan_folder('vm_coding',coding_vm_folder_id)
    do_total_column()

if __name__ == '__main__':
    main()
