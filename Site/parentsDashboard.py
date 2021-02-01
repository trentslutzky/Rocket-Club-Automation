import pg8000, time, secret

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

def main():
    db = connect()
    ps = qprep(db,"SELECT * FROM rcl_codes LIMIT 5")
    result = ps.run()
    print(result)

def main_info(member_uui):
    

if __name__ == '__main__':
    main()
