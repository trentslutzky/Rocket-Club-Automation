import RCData as rcdata
import pg8000
##### Colorama library to make pretty terminal #####
from colorama import init
init()
from colorama import Fore, Back, Style
####################################################
from rich.console import Console
from rich.table import Table
########## Trivia Winners Sheet ID ##########
certs_sheet_id = '1ShBFeE4WjJJJ4tZREC-bK_vgtKfKQXbYD3QWqfpeSlM'
####################################################

def connect():
    db = pg8000.connect("postgres", 
        password="Falcon2019", 
        host='35.199.36.16', 
        port=5432, 
        database='rocket_club')
    return db

def qprep(db, string):
    db.run("DEALLOCATE ALL")
    result = db.prepare(string)
    return result

table = Table(title = 'Certifications')
table.add_column('Entrepreneurship', no_wrap=True)
table.add_column('Robotics', no_wrap=True)
table.add_column('Tech & Programming', no_wrap=True)

console = Console()

def fix_string(string):
    string = string.lower()
    string = string.replace(' ','_')
    string = string.replace(',','')
    string = string.replace('_&_','_')
    string = string.replace('/','')
    string = string.replace(':','')
    return string

def get_certs():
    print('Getting certifications!')
    certs = rcdata.get_cells(
            certs_sheet_id, 
            'certs_range',
            'Certifications')

    entre_certs = []
    robotics_certs = []
    tech_certs = []

    for cert in certs:
        if cert[0] != '':
            clean_cert = fix_string(cert[0])
            entre_certs.append([cert[0],clean_cert])
        if cert[1] != '':
            clean_cert = fix_string(cert[1])
            robotics_certs.append([cert[1],clean_cert])
        if cert[2] != '':
            clean_cert = fix_string(cert[2])
            tech_certs.append([cert[2],clean_cert])
        table.add_row(cert[0],cert[1],cert[2])

    for e_cert in entre_certs:
        db = connect()
        command = "INSERT INTO certifications(category,cert,flair) VALUES('%s','%s','%s')" % (
                'entrepreneurship',str(e_cert[1]),str(e_cert[0]))
        db.run(command)
        db.commit()
        db.close()

    for r_cert in robotics_certs:
        db = connect()
        command = "INSERT INTO certifications(category,cert,flair) VALUES('%s','%s','%s')" % (
                'robotics',str(r_cert[1]),str(r_cert[0]))
        db.run(command)
        db.commit()
        db.close()

    for t_cert in tech_certs:
        db = connect()
        command = "INSERT INTO certifications(category, cert,flair) VALUES('%s','%s','%s')" % (
                'tech',str(t_cert[1]),str(t_cert[0]))
        db.run(command)
        db.commit()
        db.close()

    console.print(table)


def main():
    print('This could cause serious issues. Check the code before running! (N/y) ',end='')
    answer = input()
    if(answer == 'y'):
        #get_certs()
        print('get_certs')
    else:
        print('quitting.')



            
if __name__ == '__main__':
    main()
