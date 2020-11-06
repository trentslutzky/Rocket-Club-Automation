#################/ ########  IMPORTS  #################################
import pg8000
import time
from time import sleep
import datetime
from datetime import date
# Initialize Colorama for pretty terminal colors #
from colorama import init
init()
from colorama import Fore, Back, Style
#####################################################################
## connecting to the database as the root user 'postgres'

## setup the 'week_string' which is used to compare the current week to the 
 # weekly status of the virtual missions.
year = datetime.date.today().year
week_number = datetime.date.today().isocalendar()[1]
week_string = str(year)+str(week_number)
week_int = int(week_string)

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
    db = connect()
    try:
        ps = qprep(db,'SELECT member_uuid FROM members WHERE member_id=:v')
        result = ps.run(v=member_id)
        return result[0][0]
    except:
        return -1
    db.close()

## retrieve the vm_tag given sheet_id
def get_vm_tag(sheet_id):
    db = connect()
    try:
        ps = qprep(db,'SELECT vm_tag FROM virtual_missions WHERE sheet_id=:v')
        result = ps.run(v=sheet_id)
        return result[0][0]
    except:
        return -1
    db.close()

## add a new rf_transaction row based on member_id, type, subtype and amount
def add_rf_transaction(member_id,mtype,subtype,amount):
    db = connect()
    print(Fore.WHITE + 'adding RF ' + str(member_id) + '...')
    # convert member id to ssid
    uuid = get_member_uuid(int(member_id))
    if(uuid != -1):
        command = "INSERT INTO rf_transactions(member_uuid,type,subtype,amount) VALUES('%s','%s','%s',%i)" % (
                uuid,mtype,subtype,int(amount))
        db.run(command)
        db.commit()
    else:
        print('Member ID not found. Skipping.')
    db.close()

def add_vm_completion(member_id,vm_tag,category):
    db = connect()
    uuid = get_member_uuid(int(member_id))
    ps = qprep(db,'SELECT vm_tag FROM vm_completions WHERE member_uuid = :a')
    probe = ps.run(a=uuid)
    is_completed = False
    
    for tag in probe:
        if tag[0] == vm_tag:
            is_completed = True

    if(not is_completed):
        print(str(member_id) + ' Completed ' + vm_tag + '!')
        ps = qprep(db,'INSERT INTO vm_completions(member_uuid,vm_tag,category) VALUES(:a,:b,:c)')
        ps.run(a=uuid,b=vm_tag,c=category)
        db.commit()

    db.close()
    return is_completed

## get which missions are the missions for the current week
def get_weekly_missions():
    db = connect()
    ps = qprep(db,'SELECT vm_tag FROM virtual_missions WHERE week=:v')
    result = ps.run(v=week_string)
    db.close()
    return result

## get the member name, team, and division based on member_id
def get_member_info(member_id):
    db = connect()
    ps = qprep(db,'SELECT name,team,division FROM members WHERE member_id=:v')
    result = ps.run(v=member_id)
    db.close()
    return result1


###########################################################################
##################      STUFF FOR MEMBER STATS     ########################
###########################################################################

def get_member_info(member_id):
    db = connect()
    ps = qprep(db,"SELECT name,division,team from members where member_id = :a")
    result = ps.run(a=member_id)
    result[0][1] = 'Division ' + str(result[0][1])
    db.close()
    return result[0]

def get_member_total(member_id):
    db = connect()

    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a")
    result = ps.run(a=member_id)
    db.close()
    return result[0][0]

def get_vm_rf(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:d and type='virtual_mission'")
    result.append(ps.run(d=member_id)[0][0])
    db.close()
    return result[0]

def get_vm_rf_sum(member_id, subtype):
    db = connect()
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:d and subtype=:s")
    q = ps.run(d=member_id,s=subtype)
    if(q[0][0] is not None):
        result = q[0][0]
    else:
        result = 0
    return result

def get_vm_rf_categories(member_id):
    results = []
    uuid = get_member_uuid(member_id)
    # robotics
    results.append(get_vm_rf_sum(member_id,'rob_ov'))
    # coding
    results.append(get_vm_rf_sum(member_id,'python_1'))
    # engineering
    results.append(get_vm_rf_sum(member_id,'engineering'))
    # entrepreneurship
    results.append(get_vm_rf_sum(member_id,'ent_1'))
    # past
    results.append(get_vm_rf_sum(member_id,'other') + get_vm_rf_sum(member_id,'past'))
    # extra 
    results.append(get_vm_rf_sum(member_id,'extra'))
    return results

def get_member_vms_completed(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='rob_ov';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='coding_ov';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='python_1';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='robotics_1';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE member_id=:a AND category='ent_1';")
    result.append(ps.run(a=member_id)[0][0])
    db.close()
    return(result)

def get_member_rcl_rf(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='attendance'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='trivia'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='parents_night'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='launchpad'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcl' and subtype='tech_tuesday'")
    result.append(ps.run(a=member_id)[0][0])
    db.close()
    return result

def get_member_misc_rf(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='boost'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='rcgt'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='wheel_of_names'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN members ON rf_transactions.member_uuid=members.member_uuid WHERE member_id=:a and type='class'")
    result.append(ps.run(a=member_id)[0][0])
    db.close()
    return result
###########################################################################
###################      STUFF FOR TEAM STATS     #########################
###########################################################################

def get_team_members(team_name):
    db = connect()
    result = []
    ps = qprep(db,"SELECT name FROM members where team=:a")
    names = ps.run(a=team_name)
    for name in names:
        result.append(name[0])
    db.close()
    return result

def get_instructor(team_name):
    db = connect()
    ps = qprep(db,"SELECT instructor FROM teams where team_name=:a")
    result = ps.run(a=team_name)
    db.close()
    return result[0][0]

def get_weekly_missions():
    db = connect()
    result = []
    ps = qprep(db,"SELECT vm_tag,description FROM virtual_missions WHERE week=:a")
    weekly_missions = ps.run(a=week_string)
    for vm in weekly_missions:
        result.append(vm[1])
    db.close()
    return result

def get_current_weekly_missions_completed(team_name):
    db = connect()
    ps = qprep(db,"SELECT vm_tag,description FROM virtual_missions WHERE week=:a")
    weekly_missions = ps.run(a=week_string)
    result = []
    for vm in weekly_missions:
        tag = vm[0]
        ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and vm_tag=:b")
        result.append(ps.run(a=team_name,b=tag)[0][0])
    db.close()
    return result

def get_team_vms_completed(team_name):
    db = connect()
    result = []
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='rob_ov'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='coding_ov'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='python_1'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='robotics_1'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN members ON vm_completions.member_uuid=members.member_uuid WHERE team=:a and category='ent_1'")
    result.append(ps.run(a=team_name)[0][0])
    db.close()
    return result

###########################
###  Leaderboard Stuff  ###
###########################

def get_team_standings():
    db = connect()
    result = []
    standing = []
    for d in range(1,4):
        ps = qprep(db,"SELECT team,count(DISTINCT vm_completions.member_uuid) FROM vm_completions LEFT JOIN members ON members.member_uuid = vm_completions.member_uuid LEFT JOIN virtual_missions ON virtual_missions.vm_tag = vm_completions.vm_tag LEFT JOIN rf_transactions ON rf_transactions.member_uuid = members.member_uuid WHERE members.division=:a AND amount>20 AND virtual_missions.week = :w GROUP BY team ORDER BY count(DISTINCT vm_completions.member_uuid) desc limit 6;")
        standing = ps.run(a=d,w=str(week_int-1))
        for team in standing:
            ps = qprep(db,"SELECT COUNT(*) FROM members WHERE team=:a")
            team.append(ps.run(a=team[0])[0][0])
        
        standing_percentage = []
        for team in standing:
            percentage = (team[1]/team[2]) * 100
            percentage = int(round(percentage, -1))
            standing_percentage.append([team[0],percentage])

        standing_percentage = sorted(standing_percentage, key=lambda standing_percentage: standing_percentage[1], reverse=True)
        result.append(standing_percentage)   

    for d in result:
        for team in d:
            team[0] = team[0][:13]

    db.close()
    return result

def get_division_standings():
    db = connect()
    result = [] 
    for d in range(1,4):
        ps = qprep(db,"SELECT name,sum(amount) FROM rf_transactions LEFT JOIN members ON members.member_uuid = rf_transactions.member_uuid WHERE division = :a GROUP BY name ORDER BY sum(amount) desc limit 3;")
        got = ps.run(a=d)
        result.append(got)
        for a in got:
            a[1] =str(format(int(a[1]),','))
    db.close()
    return result

def get_legacy_leaders():
    db = connect()
    ps = qprep(db,'SELECT members.name,sum(rf_transactions.amount) FROM rf_transactions RIGHT JOIN members ON members.member_uuid = rf_transactions.member_uuid GROUP BY members.name ORDER BY sum(rf_transactions.amount) desc LIMIT 10;')
    result = ps.run()
    for member in result:
        member[1] =str(format(int(member[1]),','))

    db.close()
    return result

def get_trivia_leaders():
    db = connect()
    ps = qprep(db,"SELECT members.name,sum(rf_transactions.amount) FROM rf_transactions RIGHT JOIN members ON members.member_uuid = rf_transactions.member_uuid WHERE subtype = 'trivia' GROUP BY members.name ORDER BY sum(rf_transactions.amount) desc LIMIT 5;")
    result = ps.run()
    for member in result:
        member[1] =str(format(int(member[1]),','))

    db.close()
    return result

def get_parents_night_leaders():
    db = connect()
    ps = qprep(db,"SELECT members.name,sum(rf_transactions.amount) FROM rf_transactions RIGHT JOIN members ON members.member_uuid = rf_transactions.member_uuid WHERE subtype = 'parents_night' GROUP BY members.name ORDER BY sum(rf_transactions.amount) desc LIMIT 5;")
    result = ps.run()
    for member in result:
        member[1] =str(format(int(member[1]),','))
    db.close()
    return result

# ADMIN TOOLS

def get_teams():
    db = connect()
    teams = []
    results = db.run('SELECT team_name FROM teams ORDER BY team_name')
    for team in results:
        teams.append(team[0])
    return teams
    db.close()

def get_next_member_id():
    db = connect()
    ps = qprep(db,"SELECT member_id FROM members ORDER BY member_id DESC LIMIT 1")
    result = ps.run()
    db.close()
    return result[0][0]+1

def add_new_member(name,division,team):
    member_id = get_next_member_id()
    db = connect()
    command = "INSERT INTO members(member_id, name, team, division) VALUES(%i,'%s','%s',%i)" % (int(member_id),name,team,int(division))
    db.run(command)
    db.commit()
    sleep(1)
    uuid = get_member_uuid(member_id)
    print(uuid)
    command = "INSERT INTO rf_transactions(member_uuid,type,amount) VALUES('%s','base_rf',250)" % (str(uuid))
    db.run(command)
    db.commit()
    db.close()

 # Add-RF

def get_types():
    db = connect()
    results = []
    types = db.run("SELECT DISTINCT type from rf_transactions where not type in('virtual_mission','test','purchase','base_rf','rcl')")
    for type in types:
        results.append(type[0])
    return results

def get_member_name(member_id):
    db = connect()
    try:
        name = db.run("SELECT name FROM members where member_id = %i" % member_id)
        return name[0][0]
    except:
        return None

@timer
def main():
    print(week_string)

if __name__ == '__main__':
    main()





























