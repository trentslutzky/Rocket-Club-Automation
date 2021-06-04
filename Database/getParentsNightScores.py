import RCData as rcdata
import pgTool as pgtool
import re
import secret
import pg8000

from colorama import init
init()
from colorama import Fore, Back, Style

folder_id = "'11ihI-LhpXHOfV7hSNw8D3v08hvaCs8E0'"

def indicator():
    print(Fore.WHITE+'['+Fore.YELLOW+' kahoot '+Fore.WHITE+']',end=' ')

def connect():
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])
    db.run("SET TIMEZONE = 'EST'")
    return db

def kahoot_rf(db,winners,date):
    for w in winners:
        db.run(f"INSERT INTO rf_transactions(member_uuid,type,subtype,amount,completed) VALUES('{w[0]}','rcl','parents night',{w[1]},'{date}')")

def kahoot_score(db,member_uuid,kahoot,score,date):
    COMMAND = f"INSERT INTO kahoot_scores(member_uuid,kahoot,score,timestamp) VALUES('{member_uuid}','{kahoot}',{score},'{date}')"
    db.run(COMMAND)

def scan_folder():
    new_q = folder_id + " in parents"
    results = rcdata.drive_service.files().list(q = new_q, 
                                    fields='files(id, name)',
                                    pageToken=None).execute() 
    return results.get('files', [])

def main():
    print(Fore.BLUE+'Looking for new parents night kahoot sheets...')
    updated = 0
    db = connect()
    for sheet in rcdata.scan_folder(folder_id):
        sheet_id = sheet['id']
        sheet_name = sheet['name']
        if '[TRACKED]' not in sheet_name:
            score_data = rcdata.get_cells(sheet_id,'Final Scores!C4:D',sheet_name)
            date = rcdata.get_cells(sheet_id,'B2','date')[0][0] + ' 18:30'
            winners = ['','','']
            for line in score_data:
                member_id,score = line
                member_info = pgtool.get_member_info(member_id)
                member_uuid = pgtool.get_member_uuid(member_id)
                indicator()
                print(score,'to',member_info[0],end=' ')
                kahoot_score(db,member_uuid,sheet_name,score,date)
                if score_data.index(line) == 0: 
                    winners[0] = [member_uuid,3000]
                    print(Fore.GREEN+'first')
                elif score_data.index(line) == 1:
                    winners[1] = [member_uuid,1000]
                    print(Fore.GREEN+'second')
                elif score_data.index(line) == 2:
                    winners[2] = [member_uuid,500]
                    print(Fore.GREEN,'third')
                else:
                    print('')
            kahoot_rf(db,winners,date)
            rcdata.rename_sheet(sheet_id,'[TRACKED] '+sheet_name)
            updated = updated + 1
    if updated == 0:
        indicator()
        print('Nothing new here!')
    db.commit()
    db.close()
    return updated

if __name__ == '__main__':
    main()
