#########################  IMPORTS  #################################
import pg8000
import time
import datetime
from datetime import date
# Initialize Colorama for pretty terminal colors #
from colorama import init
init()
from colorama import Fore, Back, Style
#####################################################################
## connecting to the database as the root user 'postgres'
db = pg8000.connect("postgres", 
        password="Falcon2019", 
        host='35.199.36.16', 
        port=5432, 
        database='rocket_club')

## setup the 'week_string' which is used to compare the current week to the 
 # weekly status of the virtual missions.
year = datetime.date.today().year
week_number = datetime.date.today().isocalendar()[1]
week_string = str(year)+str(week_number)

def timer(function):
    def rapper():
        start_time = time.time_ns()
        function()
        end_time = time.time_ns()
        time_elapsed = (str(int((end_time-start_time) / 1000000)) + 'ms')
        print(time_elapsed)
    return rapper
## retrieve the member_uuid from the members table based on member_id
def get_member_uuid(member_id):
    try:
        ps = db.prepare('SELECT member_uuid FROM members WHERE member_id=:v')
        result = ps.run(v=member_id)
        return result[0][0]
    except:
        return -1

## retrieve the vm_tag given sheet_id
def get_vm_tag(sheet_id):
    try:
        ps = db.prepare('SELECT vm_tag FROM virtual_missions WHERE sheet_id=:v')
        result = ps.run(v=sheet_id)
        return result[0][0]
    except:
        return -1

## add a new rf_transaction row based on member_id, type, subtype and amount
def add_rf_transaction(member_id,mtype,subtype,amount):
    print(Fore.WHITE + 'adding RF ' + str(member_id) + '...')
    # convert member id to ssid
    uuid = get_member_uuid(int(member_id))
    if(uuid != -1):
        ps = db.prepare('INSERT INTO rf_transactions(member_uuid,type,subtype,amount) VALUES(:a,:b,:c,:d)')
        ps.run(a=uuid,b=mtype,c=subtype,d=amount)
        db.commit()
    else:
        print('Member ID not found. Skipping.')

def add_vm_completion(member_id,vm_tag,category):
    uuid = get_member_uuid(int(member_id))
    ps = db.prepare('SELECT vm_tag FROM vm_completions WHERE member_uuid = :a')
    probe = ps.run(a=uuid)
    is_completed = False
    
    for tag in probe:
        if tag[0] == vm_tag:
            is_completed = True

    if(not is_completed):
        print(str(member_id) + ' Completed ' + vm_tag + '!')
        ps = db.prepare('INSERT INTO vm_completions(member_uuid,vm_tag,category) VALUES(:a,:b,:c)')
        ps.run(a=uuid,b=vm_tag,c=category)
        db.commit()

    return is_completed

## get which missions are the missions for the current week
def get_weekly_missions():
    ps = db.prepare('SELECT vm_tag FROM virtual_missions WHERE week=:v')
    result = ps.run(v=week_string)
    return result

## get the member name, team, and division based on member_id
def get_member_info(member_i):
    ps = db.prepare('SELECT name,team,division FROM members WHERE member_id=:v')
    result = ps.run(v=member_id)
    return result1


###########################################################################
##################      STUFF FOR MEMBER STATS     ########################
###########################################################################

def get_member_info(member_id):
    ps = db.prepare("SELECT name,division,team from members where member_id = :a")
    result = ps.run(a=member_id)
    result[0][1] = 'Division ' + str(result[0][1])
    return result[0]

def get_member_total(member_id):
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a")
    result = ps.run(a=member_id)
    return result[0][0]

def get_vm_total_rf(member_id):
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:d and type='virtual_mission'")
    result = ps.run(d=member_id)[0][0]
    return result

def get_member_vms_completed(member_id):
    result = []
    ps = db.prepare("SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='rob_ov';")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='coding_ov';")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='python_1';")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='robotics_1';")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='ent_1';")
    result.append(ps.run(a=member_id)[0][0])
    return(result)

def get_member_rcl_rf(member_id):
    result = []
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl'")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='attendance'")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='trivia'")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='parents_night'")
    result.append(ps.run(a=member_id)[0][0])
    return result

def get_member_misc_rf(member_id):
    result = []
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='boost'")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcgt'")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='wheel_of_names'")
    result.append(ps.run(a=member_id)[0][0])
    ps = db.prepare("SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='class'")
    result.append(ps.run(a=member_id)[0][0])
    return result
###########################################################################
###################      STUFF FOR TEAM STATS     #########################
###########################################################################

def get_team_members(team_name):
    result = []
    ps = db.prepare("SELECT name FROM members where team=:a")
    names = ps.run(a=team_name)
    for name in names:
        result.append(name[0])
    return result

def get_instructor(team_name):
    ps = db.prepare("SELECT instructor FROM teams where team_name=:a")
    result = ps.run(a=team_name)
    return result[0][0]

def get_weekly_missions():
    result = []
    ps = db.prepare("SELECT vm_tag,description FROM virtual_missions WHERE week=:a")
    weekly_missions = ps.run(a=week_string)
    for vm in weekly_missions:
        result.append(vm[1])
    return result

def get_current_weekly_missions_completed(team_name):
    ps = db.prepare("SELECT vm_tag,description FROM virtual_missions WHERE week=:a")
    weekly_missions = ps.run(a=week_string)
    result = []
    for vm in weekly_missions:
        tag = vm[0]
        ps = db.prepare("SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and vm_tag=:b")
        result.append(ps.run(a=team_name,b=tag)[0][0])
    return result

def get_team_vms_completed(team_name):
    result = []
    ps = db.prepare("SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='rob_ov'")
    result.append(ps.run(a=team_name)[0][0])
    ps = db.prepare("SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='coding_ov'")
    result.append(ps.run(a=team_name)[0][0])
    ps = db.prepare("SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='python_1'")
    result.append(ps.run(a=team_name)[0][0])
    ps = db.prepare("SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='robotics_1'")
    result.append(ps.run(a=team_name)[0][0])
    ps = db.prepare("SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='ent_1'")
    result.append(ps.run(a=team_name)[0][0])
    return result

@timer
def main():
    add_rf_transaction(3115,'wheel_of_names','',5000)

if __name__ == '__main__':
    main()



