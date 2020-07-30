import RCData as rcdata
from colorama import Fore, Back, Style

rcl_attendance_folder_id = "'1eReiKr3gCD0G6W8SUGfWfzhFWW7WCvHM'"

def parse_score(scoreString):
    scoreSplit = str(scoreString).split()
    score = int(scoreSplit[0])
    return score

def get_sheets():
    new_q = rcl_attendance_folder_id + " in parents "
    results = rcdata.drive_service.files().list(q = new_q,
                                        fields='nextPageToken, files(id,name)',
                                        pageToken=None).execute()
    return results.get('files', [])

def scan_sheets():
    master_data = rcdata.get_cells(rcdata.master_sheet_id, 'A2:1000')
    master_attendance_col = master_data[0].index('rc_live_attendance')
    master_id_col = master_data[0].index('member_id')
    sheets = get_sheets()
    for sheet in sheets:
        sheet_id = sheet['id']
        sheet_name = sheet['name']
        print(Fore.BLUE + 'Scanning ' + Fore.WHITE + sheet_name)
        current_sheet = rcdata.get_cells(sheet['id'],'A1:1000') 
            # figure out which colum has the member id numbers
        id_index = 0
        for col in current_sheet[0]:
            if 'Member ID' in col:
                id_index = current_sheet[0].index(col)
            if 'Score' in col:
                score_index = current_sheet[0].index(col)
            #
        sheet_needs_updating = False
        for row in current_sheet:
            if(current_sheet.index(row) > 0):
                member_id = row[id_index]
                if('#' not in member_id):
                    sheet_needs_updating = True
                    score = parse_score(str(row[score_index]))
                        #    
                    print('    ' + Fore.YELLOW + str(member_id) + Fore.WHITE + ' got ' + Fore.YELLOW + str(score) + Fore.WHITE + ' rocket fuel')
                        # add rocket fuel to the correct cell in the master sheet
                    for master_row in master_data:
                        if master_row[master_id_col] == member_id:
                            master_row[master_attendance_col] = str(int(master_row[master_attendance_col]) + score)
                    row[id_index] = '#' + row[id_index]
        if sheet_needs_updating:
            print(Fore.WHITE + '    Updating sheet -> ', end = '  ')
            rcdata.set_cells(sheet['id'],'A1:1000',current_sheet)
        else:
            print(Fore.WHITE + '    No new data.')
    rcdata.set_cells(rcdata.master_sheet_id,'A2:1000',master_data)

def main():
    print(Fore.BLUE + '###################################')
    print(Fore.BLUE + '####  Updating RCL Attendance  ####')
    print(Fore.BLUE + '###################################')
    scan_sheets()

if __name__ == '__main__':
    main()











