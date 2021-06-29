################/ ########  IMPORTS  #################################
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

## SLACK BOT STUFF

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
client = WebClient(token=secret.app_token)                 
# ID of channel you want to post message to    
channel_id = "C023AUQ5GN8"

def send_message(channel,message):
    try:                                           
        # Call the conversations.list method using the WebClient
        result = client.chat_postMessage(
            channel=channel,
            text=message         
            # You could also use a blocks[] array to send richer content
        )                               
        # Print result, which includes information about the message (like TS)
        print(result)

    except SlackApiError as e:
        print(f"Slack Error: {e}")

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

def remove_rf_transaction(member_uuid,transaction_id):
    db = connect()
    # test if rf_transaction exists
    test = db.run(f"SELECT count(*) FROM rf_transactions WHERE member_uuid = '{member_uuid}' AND transaction_id = {transaction_id};")[0][0]
    if test == 0:
        return -1
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
    total_rf = db.run(f"select sum(amount) from rf_transactions where member_uuid = '{member_uuid}'")[0][0]
    rcl_attendance = db.run(f"SELECT count(*) from rcl_attendance_credits where member_uuid = '{member_uuid}'")[0][0]
    total_rf = int(total_rf)
    total_rf = "{:,}".format(total_rf)
    member_list = ps.run(a=member_uuid)
    db.close()
    result = []
    for member in member_list:
        result.append({
            'rcl_attendance':rcl_attendance,
            'total_rf':total_rf,
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
    ps = qprep(db,"SELECT type,amount,completed,subtype,transaction_id from rf_transactions where member_uuid = :a order by transaction_id desc limit 20")
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
            'subtype':t[3],
            'transaction_id':t[4]
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

def get_top_rf():
    output = []
    db = connect()
    COMMAND = "select b.name,a.sum from (select member_uuid,sum(amount) from rf_transactions group by member_uuid) a left join (select * from rc_members) b on a.member_uuid=b.member_uuid where b.team != 'Admin' and b.enrolled = True order by sum desc limit 10"
    result = db.run(COMMAND)
    for line in result:
        amount = "{:,}".format(line[1])
        output.append({'place':result.index(line)+1,
            'name':line[0],
            'rf':amount})
    db.close()
    return(output)

def get_current_month():
    db = connect()
    result = db.run("SELECT TO_CHAR(current_timestamp, 'Month')")[0][0].replace(' ','')
    db.close()
    return(result)

def get_top_rf_monthly():
    output = []
    db = connect()
    COMMAND = "select b.name,a.sum from (select member_uuid,sum(amount) from rf_transactions where extract(month from completed) = extract(month from now()) group by member_uuid) a left join (select * from rc_members) b on a.member_uuid=b.member_uuid where b.team != 'Admin' and b.enrolled = True order by sum desc limit 10"
    result = db.run(COMMAND)
    for line in result:
        amount = "{:,}".format(line[1])
        output.append({'place':result.index(line)+1,
            'name':line[0],
            'rf':amount})
    db.close()
    return(output)

def get_kahoot_monthly():
    db = connect()
    output = []
    COMMAND = "select name,sum,team from (select member_uuid,sum(score) from kahoot_scores where extract(month from timestamp) = extract(month from now()) group by kahoot_scores.member_uuid)b left join (select * from rc_members)a on a.member_uuid = b.member_uuid where team not in ('Admin','instructor') order by sum desc limit 10"
    result = db.run(COMMAND)
    for line in result:
        score = "{:,}".format(line[1])
        output.append({'place':result.index(line)+1,
            'name':line[0],
            'score':score})
    db.close()
    return(output)

def get_lifetime_kahoot():
    db = connect()
    output = []
    COMMAND = "select name,sum,team from (select member_uuid,sum(score) from kahoot_scores group by kahoot_scores.member_uuid)b left join (select * from rc_members)a on a.member_uuid = b.member_uuid order by sum desc limit 10"
    result = db.run(COMMAND)
    for line in result:
        score = "{:,}".format(line[1])
        output.append({'place':result.index(line)+1,
            'name':line[0],
            'score':score})
    db.close()
    return(output)

def get_monthly_attendance():
    db = connect()
    output = []
    COMMAND = "select name,count from (select member_uuid,count(*) from rcl_attendance_credits where extract(month from timestamp) = extract(month from now()) group by member_uuid) a left join (select member_uuid,name,team from rc_members) b on a.member_uuid=b.member_uuid where team not in ('','DROP','Admin','instructor') order by count desc limit 10"
    result = db.run(COMMAND)
    for line in result:
        score = "{:,}".format(line[1])
        output.append({'place':result.index(line)+1,
            'name':line[0],
            'score':score})
    db.close()
    return(output)

def get_team_RF_monthly():
    db = connect()
    output = []
    COMMAND = "select b.team,sum(amount) from (select * from rf_transactions where extract(month from completed) = extract(month from now()))a left join (select member_uuid,team from rc_members)b on a.member_uuid = b.member_uuid  where team not in ('Admin','instructor','DROP','') group by team order by sum desc limit 10"
    result = db.run(COMMAND)
    for line in result:
        score = "{:,}".format(line[1])
        output.append({'place':result.index(line)+1,
            'name':line[0],
            'score':score})
    db.close()
    return(output)

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
    result = []
    for member in member_list:
        member_uuid = get_member_uuid(member[0])
        added = db.run(f"select to_char(completed,'Mon DD HH12:MIpm') from rf_transactions where type='base_rf' and member_uuid = '{member_uuid}'")[0][0]
        result.append({
            'id':member[0],
            'name':member[1],
            'division':member[2],
            'team':member[3],
            'added':added
            })
    db.close()
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

def update_parent_payment(member_uuid,tuition,scholarship):
    db = connect()
    db.run(f"UPDATE parents SET tuition = {tuition} where assoc_member = '{member_uuid}'")
    db.run(f"UPDATE parents SET scholarship = {scholarship} where assoc_member = '{member_uuid}'")
    db.commit()
    db.close()

def get_member(member_uuid):
    db = connect()
    result = db.run("select * from rc_members where member_uuid = {member_uuid}")
    for r in result:
        print(r)

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

def get_member_name(member_uuid):
    db = connect()
    try:
        name = db.run(f"SELECT name FROM rc_members where member_uuid = '{member_uuid}'")
        db.close()
        return name[0][0]
    except:
        db.close()
        return None

def get_parent(member_uuid):
    db = connect()
    COMMAND = f"select name,email,phone,temp_password,tuition,scholarship from parents where assoc_member = '{member_uuid}' limit 1;"
    result = db.run(COMMAND)
    if result:
        parent = {
                'name':result[0][0],
                'email':result[0][1],
                'phone':result[0][2],
                'temp_pw':result[0][3],
                'tuition':result[0][4],
                'scholarship':result[0][5],
                }
    else:
        parent = {
                'name':'',
                'email':'',
                'phone':'',
                'temp_pw':'',
                'tuition':'',
                'scholarship':'',
                }
    return(parent)

def update_member_awards(member_uuid,awards):
    db = connect()
    print(f'updating awards for {member_uuid}')
    new_awards = awards
    current_awards_db = db.run(f"select award from member_awards where member_uuid = '{member_uuid}'")
    current_awards = []
    for line in current_awards_db:
        current_awards.append(line[0])

    print(current_awards,new_awards)

    for a in new_awards:
        if a not in current_awards:
            print('adding',a)
            db.run(f"INSERT INTO member_awards(member_uuid,award) VALUES('{member_uuid}','{a}')")
    for a in current_awards:
        if a not in new_awards:
            print('removing',a)
            db.run(f"delete from member_awards where member_uuid='{member_uuid}' and award ='{a}'")
    db.commit()
    db.close()

def get_member_num_certs(member_uuid):
    print('get_member_num_certs')
    db = connect()
    COMMAND = f"SELECT count(*) from member_certs where member_uuid = '{member_uuid}'"
    result = db.run(COMMAND)[0][0]
    db.close()
    return result

def get_member_awards(member_uuid):
    # initialize database
    db = connect()
    
    # get member completed journeys
    COMMAND = f"SELECT award from member_awards where member_uuid = '{member_uuid}'"
    member_awards_db = db.run(COMMAND)
    member_awards = []
    for a in member_awards_db:
        member_awards.append(a[0])

    # get all journeys
    COMMAND = "SELECT * from awards"
    awards_db = db.run(COMMAND)

    awards = []

    for award in awards_db:
        line = ({
            'award':award[0],
            'flair':award[1],
            'has':False
            })
        if award[0] in member_awards:
            line['has'] = True
        awards.append(line)

    return awards


def get_member_journeys(member_uuid):
    # initialize database
    db = connect()
    
    # get member completed journeys
    COMMAND = f"SELECT cert_id from journey_completions where member_uuid = '{member_uuid}'"
    journey_completions_db = db.run(COMMAND)
    journey_completions = []
    num_certified = 0
    for j in journey_completions_db:
        journey_completions.append(j[0])
        num_certified = num_certified + 1
    percent_complete = int((num_certified / 24)*100)

    #get all journeys
    COMMAND = "SELECT * from journeys"
    journeys = db.run(COMMAND)

    #lists for both categories
    entre_journeys = []
    science_journeys = []

    for j in journeys:
        journey = {'cert_order':j[1],
                   'flair':j[3],
                   'certified':'',
                   'cert_id':j[0],
                   'category':j[2]}
        if journey['cert_id'] in journey_completions:
            journey['certified'] = 'CERTIFIED'
        if journey['category'] == 'entre':
            entre_journeys.append(journey)
        if journey['category'] == 'science_and_tech':
            science_journeys.append(journey)

    return {'entre_journeys':entre_journeys,
            'science_journeys':science_journeys,
            'percent_complete':percent_complete,
            'num_certified':num_certified}


def update_member_journeys(member_uuid,journeys):
    db = connect()
    print(f'updating certs for {member_uuid}')
    new_journeys = journeys
    current_journeys_db = db.run(f"select cert_id from journey_completions where member_uuid = '{member_uuid}'")
    current_journeys = []
    for line in current_journeys_db:
        current_journeys.append(line[0])

    print(current_journeys,new_journeys)

    for j in current_journeys:
        if(j not in new_journeys):
            db.run(f"delete from journey_completions where member_uuid = '{member_uuid}' and cert_id = '{j}'")

    for j in new_journeys:
        if(j not in current_journeys):
            db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','{j}')")

    db.commit()
    db.close()

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

def get_rcl_code_enabled():
    db = connect()
    return db.run("select enabled from rcl_attendance_enabled")[0][0]

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

def check_rcl_rewards(member_uuid):
    amount = get_rcl_attendance_credits(member_uuid)
    member_id = get_member(member_uuid)

def get_db_date():
    db = connect()
    result = db.run('select current_date')
    db.close()
    return(result[0][0])

def get_rcl_attendance():
    db = connect()
    names = []
    COMMAND = "select r.name from (select * from rcl_attendance_credits) e left join (select * from rc_members) r on e.member_uuid = r.member_uuid where code = (select code from rcl_codes where date = current_date)"
    result = db.run(COMMAND)
    for name in result:
        names.append(name[0])
    db.close()
    return names
    
def toggle_rcl_code_enabled():
    db=connect()
    enabled = not get_rcl_code_enabled()
    db.run(f"update rcl_attendance_enabled set enabled = {enabled}")
    db.commit()
    db.close()

def get_all_attendance_credits():
    db = connect()
    output = []
    COMMAND = "select name,count from (select member_uuid,count(*) from rcl_attendance_credits group by member_uuid)a left join (select * from rc_members)b on a.member_uuid = b.member_uuid where team not in ('Admin','instructor','DROP') order by count desc"
    #COMMAND = "select name,count from (select member_uuid,count(*) from rcl_attendance_credits group by member_uuid)a left join (select * from rc_members)b on a.member_uuid = b.member_uuid order by count desc"
    result = db.run(COMMAND)
    for line in result:
        output.append({'name':line[0],'count':line[1]})
    db.close()
    return output

def get_all_members():
    db = connect()
    data = db.run("select member_uuid,member_id,name,team from rc_members where team != 'DROP'")
    members = []
    for d in data:
        members.append({
            'member_uuid':d[0],
            'member_id':d[1],
            'name':d[2],
            'team':d[3],
            })
    print(members[0])
    db.close()
    return members

def get_table_dict(table_name,where_col=None,where=None,where_2_col=None,where_2=None):
    db = connect()
    table = {}
    try:
        if where_col and where and not(where_2 and where_2_col):
            rows = db.run(f"SELECT * from {table_name} where {where_col} = {where}")
        elif where_col and where and where_2_col and where_2:
            rows = db.run(f"SELECT * from {table_name} where {where_col} = {where} and {where_2_col} = {where_2}")
        else:
            rows = db.run(f"SELECT * from {table_name}")

        column_names = db.run(f"select column_name from information_schema.columns where table_name = '{table_name}'")

        for row in rows:
            col_ind = 0
            line = {}
            for r in row:
                line[column_names[col_ind][0]] = r
                col_ind = col_ind + 1

            table[rows.index(row)] = line

        return(table)
    except:
        return(-1)

def get_table_json(table_name,where_col=None,where=None,where_2_col=None,where_2=None,order=None,limit=None):
    print('GET Table JSON '+table_name)
    db = connect()
    table = {'result':[]}
    try:
        COMMAND = f"SELECT * FROM {table_name}"
        if where_col and where and not(where_2 and where_2_col):
            COMMAND = COMMAND + (f" {table_name} where {where_col} = {where}")
        elif where_2_col and where_2:
            COMMAND = COMMAND + (f" and {where_2_col} = {where_2}")
        
        if(order):
            COMMAND = COMMAND + (f" order by {order} desc")

        if(limit):
            COMMAND = COMMAND + (f" limit {limit}")

        print(COMMAND)

        rows = db.run(COMMAND)
        
        column_names = db.run(f"select column_name from information_schema.columns where table_name = '{table_name}'")

        for row in rows:
            col_ind = 0
            line = {}
            for r in row:
                line[column_names[col_ind][0]] = r
                col_ind = col_ind + 1

            table['result'].append(line)

        return(table)
    except Exception as err:
        return(err)

def get_rf_transactions_json(member_uuid):
    db = connect()
    rows = db.run(f"SELECT * from rf_transactions where member_uuid = '{member_uuid}'")
    column_names = db.run(f"select column_name from information_schema.columns where table_name = 'rf_transactions'")
    
    table = {'result':[]}

    for row in rows:
        col_ind = 0
        line = {}
        for r in row:
            line[column_names[col_ind][0]] = r
            col_ind = col_ind + 1

        table['result'].append(line)
    
    db.close()
    return(table)

def rf_transaction_exists(member_uuid,transaction_id):
    db = connect()
    result = db.run(f"select count(*) from rf_transactions where member_uuid = '{member_uuid}' and transaction_id = {transaction_id}")[0][0]
    print(result)

def get_member_info_json(member_uuid):
    db = connect()
    info = db.run(f"SELECT * FROM rc_members where member_uuid = '{member_uuid}'")
    print(info)

@timer
def main():
    print(rf_transaction_exists('619e2d83-b9b6-43fe-bbd2-f148f1d98f76',1))

if __name__ == '__main__':
    main()

