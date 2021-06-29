import pg8000
import secret

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    db.run("set timezone = 'EST'")
    return db

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

    parent = get_table_json(table_name='parents',
                            where_col='assoc_member',
                            where=member_uuid,
                            limit=1)['result'][0]

    result['result'][0]['parent'] = parent

    db.close()
    return result

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


def main():
    print(get_member_info('619e2d83-b9b6-43fe-bbd2-f148f1d98f76'))

if __name__ == '__main__':
    main()
