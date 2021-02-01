from datetime import date, timedelta
import pg8000
import random, string

today = date.today()

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

N = 8
days_to_generate = 2000

db = connect()

for d in range(days_to_generate):
    random_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    current_day = today + timedelta(days=d)
    print(random_code,current_day,d)
    command = "INSERT INTO rcl_codes(code,date) VALUES('%s','%s')" % (random_code,current_day)
    db.run(command)   
    db.commit()

db.close()
