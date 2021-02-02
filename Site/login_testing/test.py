from flask import Flask, render_template, request, url_for, redirect
import flask_login
from flask_bcrypt import Bcrypt
import time, pg8000, secret

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = 'testkey12348976'

users = secret.admin_dashboard_users

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

def get_user(email):
    db = connect()
    ps = qprep(db,"SELECT username,email,pwhash,role FROM logins WHERE email=:e")
    result = ps.run(e=email)
    if(result):
        return {
                'username':result[0][0],
                'email':result[0][1],
                'password':result[0][2],
                'role':result[0][3],
                }
    else:
        return None

class User():
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def get_role(self):
        return self.role

@login_manager.user_loader
def user_loader(username):
    print('user_loader')
    if(not get_user(username)):
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    print('request_loader')
    username = request.form.get('username')
    if(not get_user(username)):
        return
    user = User()
    user.id = username
    user_check = get_user(username)
    if(bcrypt.check_password_hash(
        user_check['password'],request.form['password'])
        ):
        return user
    else:
        return None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print('login - GET')
        return render_template('login.html')

    if request.method == 'POST':
        print('login - POST')
        username = request.form['username']
        password = request.form['password']

        user_check = get_user(username)

        if(not user_check):
            return render_template('login.html', 
                    warning = 'Invalid Username - Try again.',
                    username=username)
        if(not bcrypt.check_password_hash(user_check['password'],password)):
            return render_template('login.html', 
                    warning = 'Invalid Password - Try again.',
                    username=username)
        else:
            user=User()
            user.id=username
            flask_login.login_user(user)
            next_page = request.args.get('next')
            print(next_page)
            if not next_page:
                next_page = url_for('index')
            return redirect(next_page)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('login.html', warning = 'Logged Out')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login',
            next=request.endpoint))

@app.route('/secrety')
@flask_login.login_required
def secrety():
    return ('secret')

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
