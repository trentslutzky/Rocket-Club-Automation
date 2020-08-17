import RCData as rcdata
from colorama import Fore, Back, Style
from datetime import datetime

rcl_attendance_folder_id = "'18Tbc7xvXc0TnhmwYVbURrx_uOzFfRmR5'"

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
    sheets = get_sheets()
    data = []
    for sheet in sheets:
        current_sheet = rcdata.get_cells(sheet['id'],'A1:1000') 
            # figure out which colum has the member id numbers
        id_index = 0
        for col in current_sheet[0]:
            if 'Member ID' in col:
                id_index = current_sheet[0].index(col)
            if 'Score' in col:
                score_index = current_sheet[0].index(col)
            if 'Timestamp' in col:
                timestamp_index = current_sheet[0].index(col)
        
        sheet_needs_updating = False
        for row in current_sheet:
            if current_sheet.index(row) > 0:
                new_score = parse_score(row[score_index])
                data.append([row[timestamp_index],row[id_index],new_score])

        print(data[0][0])
        return data 

def main():
    scan_sheets()

if __name__ == '__main__':
    main()











