#################/ ########  IMPORTS  #################################
import pg8000
import time
import secret
from time import sleep
import datetime, pytz
from datetime import date,timezone
import os
import qrcode
# Initialize Colorama for pretty terminal colors #
from colorama import init
init()
from colorama import Fore, Back, Style
#####################################################################
## connecting to the database as the root user 'postgres'

from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)
import string, random, re

## setup the 'week_string' which is used to compare the current week to the 
 # weekly status of the virtual missions.
year = datetime.date.today().year
week_number = datetime.date.today().isocalendar()[1]
week_string = str(year)+str(week_number)
week_int = int(week_string)
est = pytz.timezone('US/Eastern')

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    db.run("set timezone = 'EST'")
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
## retrieve the member_uuid from the rc_members table based on member_id
def get_member_uuid(member_id):
    db = connect()
    try:
        ps = qprep(db,'SELECT member_uuid FROM rc_members WHERE member_id=:v')
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

def add_rf_transaction_uuid(member_uuid,mtype,subtype,amount):
    db = connect()
    print(Fore.WHITE + 'adding RF ' + str(member_uuid) + '...')
    command = f"INSERT INTO rf_transactions(member_uuid,type,subtype,amount) VALUES('{member_uuid}','{mtype}','{subtype}',{amount})"
    db.run(command)
    db.commit()
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
    ps = qprep(db,'SELECT name,team,division FROM rc_members WHERE member_id=:v')
    result = ps.run(v=member_id)
    db.close()
    return result


def update_member_info(member_uuid,member_id,name,team,division,grad_date):
    # get member info for checking
    db = connect()
    ps = qprep(db,'SELECT member_id,name,division,team,grad_date FROM rc_members WHERE member_uuid = :u')
    old_member_data = ps.run(u=member_uuid)
    member_id = int(member_id)
    division = int(division)
    # check if the entered member_id is the one that the member currently has.
    # if not, check if it exists already.
    if(old_member_data[0][0] != member_id and test_member_id(member_id) != 0):
        return 2 # return 2 = member_id exists

    num_updated = 0
    # update member in database if information has changed.
    if(old_member_data[0][0] != member_id):
        command = f"UPDATE rc_members SET member_id={member_id} where member_uuid='{member_uuid}'"
        db.run(command)
        num_updated = num_updated + 1
        print(command)  
    if(old_member_data[0][1] != name):
        command = f"UPDATE rc_members SET name='{name}' where member_uuid='{member_uuid}'"
        db.run(command)
        num_updated = num_updated + 1
        print(command)  
    if(old_member_data[0][2] != division):
        command = f"UPDATE rc_members SET division={division} WHERE member_uuid='{member_uuid}'"
        db.run(command)
        num_updated = num_updated + 1
        print(command)  
    if(old_member_data[0][3] != team):
        command = f"UPDATE rc_members SET team='{team}' WHERE member_uuid='{member_uuid}'"
        db.run(command)
        num_updated = num_updated + 1
        print(command)  
    if(old_member_data[0][4] != grad_date):
        command = f"UPDATE rc_members SET grad_date='{grad_date}' WHERE member_uuid='{member_uuid}'"
        db.run(command)
        num_updated = num_updated + 1
        print(command)  
    if(num_updated > 0):
        db.commit()
        return 0 # return 0 = something was updated.
    return 1 # return 1 = nothing was updated.
    db.close()

###########################################################################
##################      STUFF FOR MEMBER STATS     ########################
###########################################################################

def get_member_info(member_id):
    db = connect()
    ps = qprep(db,"SELECT name,division,team,member_id,grad_date from rc_members where member_id = :a")
    result = ps.run(a=member_id)
    db.close()
    return result[0]

def get_member_info_uuid(member_uuid):
    db = connect()
    ps = qprep(db,"SELECT * from rc_members where member_uuid = :a")
    member_list = ps.run(a=member_uuid)
    db.close()
    result = []
    for member in member_list:
        result.append({
            'uuid':member[0],
            'member_id':member[1],
            'name':member[2],
            'team':member[3],
            'division':member[4],
            'grad_date':member[6]
            })
    return result[0]

def get_recent_rf_transactions(member_uuid):
    print('Loadding rf transactions for',member_uuid)
    db = connect()
    ps = qprep(db,"SELECT type,amount,completed,subtype from rf_transactions where member_uuid = :a order by transaction_id desc limit 20")
    transactions = ps.run(a=member_uuid)
    db.close()
    results = []
    date_fmt = '%a  -  %b.%d.%Y  -  %I:%M %p'
    for t in transactions:
        t[2] = t[2].replace(tzinfo=pytz.UTC)
        results.append({
            'type':t[0],
            'amount':t[1],
            'date':t[2].strftime(date_fmt),
            'subtype':t[3]
            })
    return results

def get_member_total(member_id):
    db = connect()
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a")
    result = ps.run(a=member_id)
    db.close()
    return result[0][0]

def get_member_total_uuid(member_uuid):
    db = connect()
    ps = qprep(db,"SELECT sum(amount) FROM rf_transactions WHERE member_uuid=:a")
    result = ps.run(a=member_uuid)
    db.close()
    return result[0][0]

def get_vm_rf(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:d and type='virtual_mission'")
    result.append(ps.run(d=member_id)[0][0])
    db.close()
    return result[0]

def get_vm_rf_sum(member_id, subtype):
    db = connect()
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:d and subtype=:s")
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
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE member_id=:a AND category='rob_ov';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE member_id=:a AND category='coding_ov';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE member_id=:a AND category='python_1';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE member_id=:a AND category='robotics_1';")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT COUNT(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE member_id=:a AND category='ent_1';")
    result.append(ps.run(a=member_id)[0][0])
    db.close()
    return(result)

def get_member_rcl_rf(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcl'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcl' and subtype='attendance'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcl' and subtype='trivia'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcl' and subtype='parents_night'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcl' and subtype='launchpad'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcl' and subtype='tech_tuesday'")
    result.append(ps.run(a=member_id)[0][0])
    db.close()
    return result

def get_member_misc_rf(member_id):
    db = connect()
    result = []
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='boost'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='rcgt'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='wheel_of_names'")
    result.append(ps.run(a=member_id)[0][0])
    ps = qprep(db,"SELECT sum(rf_transactions.amount) FROM rf_transactions LEFT JOIN rc_members ON rf_transactions.member_uuid=rc_members.member_uuid WHERE member_id=:a and type='class'")
    result.append(ps.run(a=member_id)[0][0])
    db.close()
    return result
###########################################################################
###################      STUFF FOR TEAM STATS     #########################
###########################################################################

def update_attendance(team_name,attended):
    db = connect()
    members = []
    COMMAND = f"SELECT member_uuid from rc_members where team = '{team_name}'"
    member_uuids = db.run(COMMAND)
    for member_uuid in member_uuids:
        member_uuid = str(member_uuid[0])
        db.run(f"delete from rf_transactions where date(completed) = current_date and type='class' and subtype='attendance' and member_uuid='{member_uuid}'")
        db.commit()
        if str(member_uuid) in attended:
            add_rf_transaction_uuid(str(member_uuid),'class','attendance',50)
    db.close()

def get_team_members(team_name):
    db = connect()
    members = []
    COMMAND = f"SELECT name,member_id,member_uuid FROM rc_members WHERE team = '{team_name}' order by name"
    mems = db.run(COMMAND)
    for m in mems:
        member_uuid = m[2]
        COMMAND = f"select sum(amount) from rf_transactions where member_uuid = '{member_uuid}'"
        sum = db.run(COMMAND)[0][0]
        members.append(
            {'name':m[0],
             'member_id':m[1],
            'uuid':member_uuid,
            'attendance':get_attendance(member_uuid),
            'competition':get_class_subtype(member_uuid,'competition'),
            'communities':get_class_subtype(member_uuid,'communities'),
            'wheel':get_class_subtype(member_uuid,'wheel'),
            'kahoot':get_class_subtype(member_uuid,'kahoot'),
            'bonus':get_class_subtype(member_uuid,'bonus'),
            'participation':get_class_subtype(member_uuid,'participation'),
            'total_rf':sum}
        )
    db.close()
    return members

def get_current_time():
    db = connect()
    COMMAND = "SELECT now()::timestamp(0);"
    date_time_str = str(db.run(COMMAND)[0][0])
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return (date_time_obj.strftime('%m/%-d %H:%M'))

def update_class_category(member_uuid,subtype,amount):
    print('updating',subtype,'for',member_uuid)
    db = connect()
    COMMAND = (f"delete from rf_transactions where date(completed) = current_date and type='class' and subtype='{subtype}' and member_uuid='{member_uuid}'")
    db.run(COMMAND)  
    db.commit()
    db.close()
    add_rf_transaction_uuid(member_uuid,'class',subtype,amount)

def get_class_subtype(member_uuid,subtype):
    db = connect()
    ps = qprep(db,f"select sum(amount) from rf_transactions where date(completed) = current_date and type='class' and subtype='{subtype}' and member_uuid='{member_uuid}'")
    result = ps.run()
    db.close()
    if not result[0][0]:
        result[0][0] = 0
    return result[0][0]

def get_attendance(member_uuid):
    db = connect()
    ps = qprep(db,f"select count(*) from rf_transactions where date(completed) = current_date and type='class' and subtype='attendance' and member_uuid='{member_uuid}'")
    result = ps.run()
    db.close()
    if result[0][0] == 1:
        return True
    else:
        return False

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
        ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE team=:a and vm_tag=:b")
        result.append(ps.run(a=team_name,b=tag)[0][0])
    db.close()
    return result

def get_team_vms_completed(team_name):
    db = connect()
    result = []
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE team=:a and category='rob_ov'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE team=:a and category='coding_ov'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE team=:a and category='python_1'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE team=:a and category='robotics_1'")
    result.append(ps.run(a=team_name)[0][0])
    ps = qprep(db,"SELECT count(*) FROM vm_completions LEFT JOIN rc_members ON vm_completions.member_uuid=rc_members.member_uuid WHERE team=:a and category='ent_1'")
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
        ps = qprep(db,"SELECT team,count(DISTINCT vm_completions.member_uuid) FROM vm_completions LEFT JOIN rc_members ON rc_members.member_uuid = vm_completions.member_uuid LEFT JOIN virtual_missions ON virtual_missions.vm_tag = vm_completions.vm_tag LEFT JOIN rf_transactions ON rf_transactions.member_uuid = rc_members.member_uuid WHERE rc_members.division=:a AND amount>20 AND virtual_missions.week = :w GROUP BY team ORDER BY count(DISTINCT vm_completions.member_uuid) desc limit 6;")
        standing = ps.run(a=d,w=str(week_int-1))
        for team in standing:
            ps = qprep(db,"SELECT COUNT(*) FROM rc_members WHERE team=:a")
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
        ps = qprep(db,"SELECT name,sum(amount) FROM rf_transactions LEFT JOIN rc_members ON rc_members.member_uuid = rf_transactions.member_uuid WHERE division = :a GROUP BY name ORDER BY sum(amount) desc limit 3;")
        got = ps.run(a=d)
        result.append(got)
        for a in got:
            a[1] =str(format(int(a[1]),','))
    db.close()
    return result

def get_legacy_leaders():
    db = connect()
    ps = qprep(db,'SELECT rc_members.name,sum(rf_transactions.amount) FROM rf_transactions RIGHT JOIN rc_members ON rc_members.member_uuid = rf_transactions.member_uuid GROUP BY rc_members.name ORDER BY sum(rf_transactions.amount) desc LIMIT 10;')
    result = ps.run()
    for member in result:
        member[1] =str(format(int(member[1]),','))

    db.close()
    return result

def get_trivia_leaders():
    db = connect()
    ps = qprep(db,"SELECT rc_members.name,sum(rf_transactions.amount) FROM rf_transactions RIGHT JOIN rc_members ON rc_members.member_uuid = rf_transactions.member_uuid WHERE subtype = 'trivia' GROUP BY rc_members.name ORDER BY sum(rf_transactions.amount) desc LIMIT 5;")
    result = ps.run()
    for member in result:
        member[1] =str(format(int(member[1]),','))

    db.close()
    return result

def get_parents_night_leaders():
    db = connect()
    ps = qprep(db,"SELECT rc_members.name,sum(rf_transactions.amount) FROM rf_transactions RIGHT JOIN rc_members ON rc_members.member_uuid = rf_transactions.member_uuid WHERE subtype = 'parents_night' GROUP BY rc_members.name ORDER BY sum(rf_transactions.amount) desc LIMIT 5;")
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
    ps = qprep(db,"SELECT member_id FROM rc_members ORDER BY member_id DESC LIMIT 1")
    result = ps.run()
    db.close()
    return result[0][0]+1

def test_member_id(member_id):
    db = connect()
    ps = qprep(db,"SELECT COUNT(1) FROM rc_members WHERE member_id = :i")
    member_exsists = ps.run(i=member_id)
    db.close()
    return member_exsists[0][0]

def get_recent_members(num):
    db = connect()
    ps = qprep(db,"SELECT member_id,name,division,team from rc_members order by member_id desc limit :n")
    member_list = ps.run(n=num)
    db.close()
    result = []
    for member in member_list:
        result.append({
            'id':member[0],
            'name':member[1],
            'division':member[2],
            'team':member[3]
            })
    return result

def add_new_member(member_id,name,division,team,grad_date):
    db = connect()
    command = f"INSERT INTO rc_members(member_id, name, team, division, grad_date) VALUES({member_id},'{name}','{team}',{division},'{grad_date}')"
    db.run(command)
    db.commit()
    sleep(1)
    uuid = get_member_uuid(member_id)
    print(uuid)
    command = "INSERT INTO rf_transactions(member_uuid,type,amount) VALUES('%s','base_rf',250)" % (str(uuid))
    db.run(command)
    db.commit()
    db.close()

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def generate_username_from_name(name):
    username = name.replace(' ','')
    rx = re.compile('\W+')
    username = rx.sub('',username).strip()
    return username

def parent_exists(email):
    db = connect()
    count = db.run(f"select count(*) from parents where email = '{email}';")
    if count[0][0] > 0: 
        return(True)
    else:
        return(False)

def add_parent(assoc_member_id,name,email,phone,cost,scholarship):
    db = connect()
    if parent_exists(email) == False:
        temp_password = get_random_alphanumeric_string(10)
        pw_hash = bcrypt.generate_password_hash(temp_password).decode('utf-8')
    else:
        temp_password = db.run(f"select temp_password from parents where email = '{email}'")[0][0];
        pw_hash = db.run(f"select pw_hash from parents where email = '{email}'")[0][0];
    assoc_member = get_member_uuid(assoc_member_id)
    username = generate_username_from_name(name)
    print(temp_password)
    command = f"INSERT INTO parents(assoc_member,name, username, email, phone, tuition, scholarship, temp_password, pw_hash) VALUES('{assoc_member}','{name}','{username}','{email}','{phone}',{cost},{scholarship},'{temp_password}','{pw_hash}')"
    db.run(command)
    db.commit()
    db.close()

##################################################################
################     STUFF FOR EDIT MEMBER       #################
##################################################################

def search_members(query):
    db = connect()
    query = query.replace(' ','')
    ps = qprep(db,"select member_uuid,member_id,name,division,team from rc_members where to_tsvector(name||' '||member_id) || to_tsvector(team) @@ to_tsquery(:q) OR name % :q order by member_id desc;")
    member_list = ps.run(q=query)
    db.close()
    result = []
    for member in member_list:
        result.append({
            'm_uuid':member[0],
            'id':member[1],
            'name':member[2],
            'division':member[3],
            'team':member[4]
            })
    return result

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
        name = db.run("SELECT name FROM rc_members where member_id = %i" % member_id)
        return name[0][0]
    except:
        return None

def get_parent(member_uuid):
    db = connect()
    COMMAND = f"select name,email,phone,temp_password from parents where assoc_member = '{member_uuid}' limit 1;"
    result = db.run(COMMAND)
    if result:
        parent = {
                'name':result[0][0],
                'email':result[0][1],
                'phone':result[0][2],
                'temp_pw':result[0][3],
                }
    else:
        parent = {
                'name':'',
                'email':'',
                'phone':'',
                'temp_pw':'',
                }
    print(parent)
    return(parent)


# Rocket Club Live Attendance #

#create a qr code and put in the right place
def generate_qr_code(code):
    filename = 'QR_'+code+'.png'
    if (os.path.isfile('./static/rclcode/img/'+filename)):
        print('QR exists',filename)
    else:
        data = "https://www.rocketclubtools.com/rcl-attendance?code="+code
        qr = qrcode.QRCode(version=1, box_size=8, border=0)
        qr.add_data(data)
        qr.make()
        img = qr.make_image(fill_color="#FFDE59", back_color="transparent")
        img.save('./static/rclcode/img/'+filename)
        print('generated',filename)

def get_rcl_code_today():
    db = connect()
    ps = qprep(db,"SELECT code FROM rcl_codes WHERE date = current_date")
    result = ps.run()[0][0]
    generate_qr_code(result)
    return(result)

def check_code(member_id,code):
    member_uuid = get_member_uuid(member_id)
    db = connect()
    COMMAND = f"SELECT count(*) FROM rcl_attendance_credits WHERE member_uuid = '{member_uuid}' AND code = '{code}'"
    result = db.run(COMMAND)
    if result[0][0] != 0:
        return 1
    ps = qprep(db,"SELECT code FROM rcl_codes WHERE date = current_date")
    result = ps.run()
    if(result[0][0] == code):
        return 0
    else:
        return 2

def get_rcl_attendance_credits(member_uuid):
    db = connect()
    COMMAND = f"SELECT count(*) FROM rcl_attendance_credits WHERE member_uuid = '{member_uuid}'"
    result = db.run(COMMAND)[0][0]
    return result

def give_rcl_attendance_credit(member_uuid,code):
    db = connect()
    COMMAND = f"INSERT INTO rcl_attendance_credits(member_uuid,code) VALUES('{member_uuid}','{code}')"
    db.run(COMMAND)
    db.commit()
    db.close()

def get_db_date():
    db = connect()
    result = db.run('select current_date')
    return(result[0][0])

def get_rcl_attendance():
    db = connect()
    names = []
    COMMAND = "select r.name from (select * from rcl_attendance_credits) e left join (select * from rc_members) r on e.member_uuid = r.member_uuid where code = (select code from rcl_codes where date = current_date)"
    result = db.run(COMMAND)
    for name in result:
        names.append(name[0])
    return names

@timer
def main():
    print(get_parent('619e2d83-b9b6-43fe-bbd2-f148f1d98f76'))

if __name__ == '__main__':
    main()

