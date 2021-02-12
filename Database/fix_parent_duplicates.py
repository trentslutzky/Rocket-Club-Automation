import pg8000, secret

def connect():           
    db = pg8000.connect(secret.db['user'],
        password=secret.db['password'],       
        host=secret.db['host'],            
        port=secret.db['port'],            
        database=secret.db['database'])    
    return db

def qprep(db, string):
    db.run("DEALLOCATE ALL")
    result = db.prepare(string)
    return result

def get_duplicate_parents():
    db = connect()
    ps = qprep(db,"select user_id from parents group by user_id having count(*) > 1")
    result = ps.run()
    db.close()
    return result

def get_single_password(user_id):
    db = connect()
    ps = qprep(db,"SELECT pw_hash FROM parents WHERE user_id=:u LIMIT 1")
    result = ps.run(u=user_id)
    db.close()
    return result[0][0]

def update_password(user_id,password):
    db = connect()
    command = f"UPDATE parents SET pw_hash = '{password}' WHERE user_id= '{user_id}'"
    result = db.run(command)
    db.commit()
    db.close()


for parent in get_duplicate_parents():
    user_id = parent[0]
    password = get_single_password(user_id)
    update_password(user_id,password)
    print(user_id,password)
