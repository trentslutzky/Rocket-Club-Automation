import pg8000
import secret
from time import sleep

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    db.run("set timezone = 'EST'")
    return db

def get_member_awards(member_uuid):
    db = connect()

    member_awards_db = db.run(f"select award from member_awards where member_uuid = {member_uuid}")
    member_awards = []
    for a in member_awards_db:
        member_awards.append(a[0])

    all_awards_db = db.run("SELECT award,flair from awards")
    awards = []
    for a in all_awards_db:
        has = False
        if(a[0] in member_awards):
            has = True
        awards.append({
            'id':a[0],
            'flair':a[1],
            'certified':has
            })

    return(awards)
    db.close()


def get_member_info(member_uuid):
    db = connect()
    member_uuid = "'"+member_uuid+"'"
    info = db.run(f"SELECT * FROM rc_members where member_uuid = {member_uuid}")
    info_columns = db.run(f"select column_name from information_schema.columns where table_name = 'rc_members'")

    result = {'result':[]}

    for row in info:
        col_ind = 0
        line = {}
        for r in row:
            line[info_columns[col_ind][0]] = r
            col_ind = col_ind + 1

        result['result'].append(line)

    rocket_fuel = db.run(f"SELECT sum(amount) from rf_transactions where member_uuid = {member_uuid}")[0][0]
    result['result'][0]['total_rf'] = rocket_fuel

    attendance_credits = db.run(f"SELECT count(*) from rcl_attendance_credits where member_uuid = {member_uuid}")[0][0]
    result['result'][0]['rcl_attendance'] = attendance_credits

    member_journeys = get_member_journeys(member_uuid)
    print(member_journeys)

    parent = get_table_json(table_name='parents',
                            where_col='assoc_member',
                            where=member_uuid,
                            limit=1)['result'][0]

    result['result'][0]['parent'] = parent
    result['result'][0]['journeys'] = member_journeys
    result['result'][0]['awards'] = get_member_awards(member_uuid)

    db.close()
    return result

def get_all_members():
    members = get_table_json(table_name = 'rc_members')
    return(members)

def get_table_json(table_name,where_col=None,where=None,where_2_col=None,where_2=None,order=None,limit=None):
    print('GET Table JSON '+table_name)
    db = connect()
    table = {'result':[]}
    try:
        COMMAND = f"SELECT * FROM {table_name}"
        if where_col and where:
            COMMAND = COMMAND + (f" {table_name} where {where_col} = {where}")

        if where_2_col and where_2:
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

def member_id_exists(member_id):
    db = connect()
    result = db.run(f"SELECT count(*) from rc_members where member_id = {member_id}")[0][0]
    if result != 0:
        db.close()
        return(True)
    db.close()
    return(False)


def update_member_info(data):
    member_uuid = data['member_uuid']
    updated = False
    message = "No new changes."
    db = connect()
    new_name = data['name']
    new_member_id = data['member_id']
    new_division = data['division']
    new_team = data['team']

    # Get current member info to compare
    current_info = db.run(f"select name,member_id,division,team from rc_members where member_uuid = '{data['member_uuid']}'")[0]
    current_name = current_info[0]
    current_member_id = current_info[1]
    current_division = current_info[2]
    current_team = current_info[3]

    if(new_name != current_name):
        print('updating name')
        db.run(f"UPDATE rc_members SET name = '{new_name}' where member_uuid='{member_uuid}'")
        updated = True
    if(new_division != current_division):
        print('updating division')
        db.run(f"UPDATE rc_members SET division = '{new_division}' where member_uuid='{member_uuid}'")
        updated = True
    if(new_team != current_team):
        print('updating team')
        db.run(f"UPDATE rc_members SET team = '{new_team}' where member_uuid='{member_uuid}'")
        updated = True
    if(new_member_id != current_member_id):
        print('updating member_id')
        exists = member_id_exists(new_member_id)
        if(exists):
            updated = False
            message = 'That Member ID Exsists. Please try again.'
        else:
            db.run(f"UPDATE rc_members SET member_id = '{new_member_id}' where member_uuid='{member_uuid}'")
            updated = True

    if(updated):
        message = 'Updated.'

    if(updated):
        db.commit()
    db.close()
    return({'updated':updated,'message':message})

def update_parent_info(data):
    print(data)
    updated = False;
    message = 'No changes.'
    
    db = connect()
    
    member_uuid = data['member_uuid']
    new_name = data['parent_name']
    new_email = data['email']
    new_phone = data['phone']
    current_parent_info = db.run(f"SELECT name,email,phone from parents where assoc_member = '{member_uuid}'")[0]
    current_name = current_parent_info[0]
    current_email = current_parent_info[1]
    current_phone = current_parent_info[2]

    if new_name != current_name:
        db.run(f"UPDATE parents SET name = '{new_name}' where assoc_member = '{member_uuid}'");
        updated = True

    if new_email != current_email:
        db.run(f"UPDATE parents SET email = '{new_email}' where assoc_member = '{member_uuid}'");
        updated = True

    if new_phone != current_phone:
        db.run(f"UPDATE parents SET phone = '{new_phone}' where assoc_member = '{member_uuid}'");
        updated = True

    db.commit();
    db.close();

    return({'updated':updated,'message':message})

def get_member_journeys(member_uuid):
    db = connect()
    all_journeys = db.run("SELECT cert_id, flair, category FROM journeys order by cert_order")
    member_journeys_db = db.run(f"SELECT cert_id from journey_completions where member_uuid = {member_uuid}")
    member_journeys = []

    for m in member_journeys_db:
        member_journeys.append(m[0])

    result = {'entre':[],
            'science_and_tech':[],
            'num':0,
            'percentage':0}

    for j in all_journeys:
        line = {
                'cert_id':j[0],
                'flair':j[1],
                'category':j[2],
                'certified':False
                }
        if(line['cert_id'] in member_journeys):
            result['num'] = result['num'] + 1
            line['certified'] = True

        if(line['category'] == 'entre'):
            result['entre'].append(line)
        elif(line['category'] == 'science_and_tech'):
            result['science_and_tech'].append(line)

        result['percentage'] = (result['num'] / 24)*100

    return(result)
    db.close()

def update_member_journeys(data):
    updated = False
    # get importand things out of data object
    member_uuid = data['member_uuid']
    certs_data = data['result']
    new_certs = []
    for c in certs_data:
        if(c[1] == True):
            new_certs.append(c[0])

    # get current journey certifications for member
    db = connect()
    current_certs_db = db.run(f"SELECT cert_id from journey_completions where member_uuid = '{member_uuid}'")
    current_certs = []
    for c in current_certs_db:
        current_certs.append(c[0])

    print(current_certs)
    print(new_certs)
    
    # iterate over current_certs. If it is not in new certs, delete it.
    for cert in current_certs:
        if cert not in new_certs:
            updated = True
            print('remove',cert)
            db.run(f"DELETE FROM journey_completions WHERE member_uuid = '{member_uuid}' AND cert_id = '{cert}'")

    # iterate each new cert. If it is not in current certs, add it.
    for cert in new_certs:
        if cert not in current_certs:
            updated = True
            print('add',cert)
            db.run(f"INSERT INTO journey_completions(member_uuid,cert_id) VALUES('{member_uuid}','{cert}')")

    # commit and close
    db.commit()
    db.close()

    # return the status so we know if the page has updated.
    return({'updated':updated})

def update_member_awards(data):
    updated = False
    db = connect()
    member_uuid = data['member_uuid']
    member_awards = data['result']

    current_awards_db = db.run(f"SELECT award from member_awards where member_uuid = '{member_uuid}'")
    current_awards = []
    for c in current_awards_db:
        current_awards.append(c[0])

    for award in member_awards:
        if(award[1] == True):
            if(award[0] not in current_awards):
                print('add',award[0])
                updated = True
                db.run(f"INSERT INTO member_awards(member_uuid,award) VALUES('{member_uuid}','{award[0]}')")
        if(award[1] == False):
            if(award[0] in current_awards):
                print('remove',award[0])
                updated = True
                db.run(f"DELETE FROM member_awards where member_uuid = '{member_uuid}' AND award = '{award[0]}'")

    db.commit()
    db.close()
    return({'updated':updated})

def rf_transaction_exists(member_uuid,transaction_id):
    db = connect()                         
    result = db.run(f"select count(*) from rf_transactions where member_uuid = '{member_uuid}' and transaction_id = {transaction_id}")[0][0]
    db.close()
    if result > 0:
        return(True)
    else:
        return(False)

def remove_rf_transaction(member_uuid,transaction_id):
    db = connect()
    
    # check if transaction exists so we don't do anything stupid
    exists = rf_transaction_exists(member_uuid,transaction_id)
    if exists == False: 
        return -1

    db.run(f"delete from rf_transactions where member_uuid = '{member_uuid}' and transaction_id = {transaction_id};")
    transaction = get_table_json(
            table_name='rf_transactions',
            where_col='member_uuid',
            where="'"+member_uuid+"'",
            where_2_col='transaction_id',
            where_2=transaction_id,
            order='transaction_id',  
            limit=1
    )
    db.commit()
    db.close()
    return(transaction)

def get_add_member_page():
    db = connect()
    result = {}
    # get 20 most recently added members
    recent_members = get_table_json(table_name='rc_members',
            limit=20,order='member_id')['result']

    upcoming_member_id = db.run("SELECT member_id from rc_members where member_id < 9000  order by member_id desc limit 1")[0][0] + 1
    upcoming_member_id_trial = db.run("SELECT member_id from rc_members limit 1")[0][0] + 1

    teams = get_table_json(table_name='teams')['result']
    grad_dates = get_table_json(table_name='graduation_dates')['result']

    member_ids_db = db.run("SELECT member_id from rc_members")
    member_ids = []
    for m in member_ids_db:
        member_ids.append(m[0])
    print(member_ids)

    result['teams'] = teams
    result['grad_dates'] = grad_dates
    result['upcoming_member_id'] = upcoming_member_id
    result['upcoming_member_id_trial'] = upcoming_member_id_trial
    result['recent_members'] = recent_members
    result['member_ids'] = member_ids
    return(result)

def get_add_rf_page(data):
    member_uuid = data['member_uuid']
    db = connect()
    result = {}
    # get most 10 most rement rf transactions for user 
    transactions = get_table_json(
            table_name="rf_transactions",
            where_col="member_uuid",
            where=f"'{member_uuid}'",
            order="transaction_id",
            limit=10)

    communities = get_table_json(table_name="communities")

    categories = [
            {'category':'rcl','flair':'Rocket Club Live'},
            {'category':'communities','flair':'Communities'},
            {'category':'bonus','flair':'Bonus'},
            {'category':'other','flair':'Other'},
            {'category':'deduction','flair':'Deduction'},
            ]

    rcl_subcategories = [
            {'category':'kahoot_1','flair':'Kahoot 1st Place'},
            {'category':'kahoot_2','flair':'Kahoot 2nd Place'},
            {'category':'kahoot_3','flair':'Kahoot 3rd Place'},
            {'category':'wheel_of_names','flair':'Wheel of Names'},
            {'category':'wheel_birthday','flair':'Birthday Wheel'},
            {'category':'wheel_tech_tues','flair':'Techteusday Wheel'},
            {'category':'bonus','flair':'Bonus'},
            {'category':'competition','flair':'Competition'},
            {'category':'parents_1_first','flair':'Parents Night (#1) 1st Place'},
            {'category':'parents_1_second','flair':'Parents Night (#1) 2nd Place'},
            {'category':'parents_1_third','flair':'Parents Night (#1) 3rd Place'},
            {'category':'parents_2_first','flair':'Parents Night (#2) 1st Place'},
            {'category':'parents_2_second','flair':'Parents Night (#2) 2nd Place'},
            {'category':'parents_2_third','flair':'Parents Night (#2) 3rd Place'},
            {'category':'showdown','flair':'Showdown'},
            ]

    member_data = get_table_json(table_name="rc_members",where_col="member_uuid",where=f"'{member_uuid}'")

    result['transactions'] = transactions
    result['communities'] = communities
    result['categories'] = categories
    result['member_data'] = member_data
    result['rcl_subcategories'] = rcl_subcategories

    db.close()
    return(result)

def add_rf(data):
    db = connect()
    print(data)
    result = {}
    updated = True
    message = 'Updated.'
    db.run(f"INSERT INTO rf_transactions(member_uuid,type,subtype,amount) VALUES('{data['member_uuid']}','{data['category']}','{data['subcategory']}',{data['amount']})")
    result['updated'] = updated
    result['message'] = message
    db.commit()
    db.close()
    return(result)

def add_new_member(data):
    db = connect()
    updated = False
    message = ''
    print(data)

    member_id = data['member_id']
    exists = db.run(f"SELECT count(*) FROM rc_members WHERE member_id = {member_id}")[0][0]

    if(exists != 0):
        updated=False
        message='Member ID Exsists'

    result = {}
    result['updated'] = updated
    result['message'] = message
    #db.commit()
    db.close()
    return(result)

def main():
    print(get_add_member_page())

if __name__ == '__main__':
    main()
