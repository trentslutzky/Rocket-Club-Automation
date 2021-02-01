from flask import Flask
from flask_bcrypt import Bcrypt
import time, pg8000, secret

app = Flask(__name__)
bcrypt = Bcrypt(app)

def timer(function):
    def rapper():
        start_time = time.time_ns()
        function()
        end_time = time.time_ns()
        time_elapsed = (str(int((end_time-start_time) / 1000000)) + 'ms')
        print(time_elapsed)
    return rapper

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

def db_new_user(email,pw_hash):
    db = connect()
    command = "INSERT INTO login_parents(email,pw_hash) VALUES('%s','%s')" % (email,pw_hash)
    db.run(command)
    db.commit()

def get_user(email):
    db = connect()
    ps = qprep(db,"SELECT email,pw_hash FROM login_parents WHERE email=:e")
    result = ps.run(e=email)
    if(result):
        return {'email':result[0][0],'password':result[0][1]}
    else:
        return None

@timer
def main():
    email = 'trent.slutzky@gmail.com'
    password = 'hunter2'
    pw_hash = bcrypt.generate_password_hash(password)
    #db_new_user(email,pw_hash.decode('utf-8'))
    user = get_user(email)

    if(user):
        print(user)
    else:
        print('email not found')

if __name__ == '__main__':
    main()
