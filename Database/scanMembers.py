# pylint: disable=no-member
# pylint: disable=unused-variable
import RCData as rcdata
import pgTool as pgtool
from pgTool import db
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style

members_sheet_id = '1NkimepO4sGj3ykHdkeCE-MGM8uXnjtMBsbWAzNlDDH8'

def main():
    updated = False
    data = rcdata.get_cells(members_sheet_id,'Member Info!A2:1000')
    ps = db.prepare('SELECT member_id FROM members')
    current_members = ps.run()
    for row in data:
        # get information from the list as variables
        member_id = row[0]
        name = row[1]
        division = row[2]
        team = row[3]
        
        # remove non-numeric characters from the division 
        numeric_filter = filter(str.isdigit, division)
        numeric_div = ''.join(numeric_filter)
        division = numeric_div
        if division == '':
            division = '0'

        in_database = False
        for member in current_members:
            if member[0] == int(member_id):
                in_database = True
   
        if(not in_database):
            print('New Member ' + name + ' ' + member_id + ' adding to db...', end = ' ')
            ps = db.prepare('INSERT INTO members(member_id,name,team,division) VALUES(:i,:n,:t,:d)')
            ps.run(i=member_id,n=name,t=team,d=division)
            print('done')
            updated = True

    db.commit()

    if(updated == False):
        print('No New Data!')

if __name__ == '__main__':
    main()

