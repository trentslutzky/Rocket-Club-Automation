from flask import Flask, render_template, request, url_for, redirect
import flask_login
from flask_login import current_user
from flask_bcrypt import Bcrypt
import time, pg8000, secret

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
app.secret_key = secret.app_secret

users = secret.admin_dashboard_users

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

def request_user(email):
    db = connect()
    ps = qprep(db,"SELECT user_id,email,pw_hash FROM parents WHERE email=:e")
    result = ps.run(e=email)
    if(result):
        return {
                'user_id':result[0][0],
                'email':result[0][1],
                'password':result[0][2]
                }
    else:
        return None

def logged_in_check_password(password):
    user_id = flask_login.current_user.id
    current_user = get_user(user_id)
    current_hash = current_user['hash']
    return bcrypt.check_password_hash(current_hash,password)

def get_user(user_id):
    print('getting user from',user_id)
    db = connect()
    ps = qprep(db,"SELECT * FROM parents WHERE user_id=:u")
    result = ps.run(u=user_id)
    if(result):
        print('got user',result[0])
        return {
                'email':result[0][2],
                'hash':result[0][3],
                'phone':result[0][4],
                'assoc_member':result[0][5],
                'tuition':result[0][6],
                'scholarship':result[0][7],
                'name':result[0][9],
                'user_id':result[0][0]
                }
    else:
        return None

def get_user_id_from_email(email):
    db = connect()
    ps = qprep(db, "SELECT user_id from parents WHERE email=:e")
    result = ps.run(e=email)
    print('got user id from email',result[0])
    return result[0][0]

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

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def get_name(self):
        return self.name

####### Methods for authentication ########################

@login_manager.user_loader
def user_loader(user_id):
    print('user_loader',user_id)
    new_user = get_user(user_id)
    user=User()
    user.id=new_user['user_id']
    user.email=new_user['email']
    user.name=new_user['name']
    user.phone=new_user['phone']
    return user


@login_manager.request_loader
def request_loader(request):
    print('request_loader',request)
    username = request.form.get('username')
    if(not request_user(username)):
        return
    user = User()
    user_check = request_user(username)
    if(bcrypt.check_password_hash(user_check['password'],request.form['password'])):
        user.id = user_check['user_id']
        return user
    else:
        return None

#########################################################

@app.route('/')
def index():
    if (flask_login.current_user.is_authenticated):
        return redirect(url_for('dashboard'))
    else:
        return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print('login - GET')
        return render_template('login.html')

    if request.method == 'POST':
        print('login - POST')
        email = request.form['email']
        password = request.form['password']

        user_check = request_user(email)

        if(not user_check):
            return render_template('login.html', 
                    warning = 'Invalid Email - Try again.',
                    username=email)
        if(not bcrypt.check_password_hash(user_check['password'],password)):
            return render_template('login.html', 
                    warning = 'Invalid Password - Try again.',
                    username=email)
        else:
            user_id = get_user_id_from_email(email)
            new_user = get_user(user_id)
            user=User()
            user.id=new_user['user_id']
            user.email=new_user['email']
            user.name=new_user['name']
            user.phone=new_user['phone']
            flask_login.login_user(user)
            next_page = request.args.get('next')
            print(next_page)
            if not next_page:
                next_page = url_for('dashboard')
            return redirect(next_page)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

def get_students(user_id):
    db=connect()
    ps = qprep(db,"SELECT assoc_member FROM parents WHERE user_id=:u")
    member_ids = ps.run(u=user_id)
    students = []
    for member_id in member_ids:
        m = member_id[0]
        ps = qprep(db,"SELECT name,member_id,team,division,grad_date from rc_members where member_uuid=:u")
        result = ps.run(u=member_id[0])
        team_name = result[0][2]
        team = get_team(team_name)
        students.append({
                'name':result[0][0],
                'member_id':result[0][1],
                'team':team,
                'division':result[0][3],
                'grad_date':result[0][4]})
    db.close()
    return students

def get_membership(user_id):
    db = connect()
    ps = qprep(db,"SELECT tuition,scholarship from parents where user_id=:u LIMIT 1")
    result = ps.run(u=user_id)
    return {
            'tuition':result[0][0],
            'scholarship':result[0][1],
            'cost':result[0][0]-result[0][1]}
    db.close()

def get_team(team_name):
    db = connect()
    ps = qprep(db,"SELECT team_name,instructor,day,time FROM teams WHERE team_name=:n")
    team = ps.run(n=team_name)
    instructor = team[0][1]
    ps = qprep(db,f"SELECT * from zoom_links where name = '{instructor}'")
    zoom = ps.run()
    return {
            'team_name':team[0][0],
            'instructor':instructor,
            'zoom_link':zoom[0][1],
            'zoom_password':zoom[0][2],
            'day':team[0][2],
            'time':team[0][3]}
    db.close()

@app.route('/dashboard', methods=['GET','POST'])
@flask_login.login_required
def dashboard():
    user_id = flask_login.current_user.id
    students = get_students(user_id)
    membership = get_membership(user_id)
    receipt_confirmation = ''
    user = get_user(user_id)
    email = user['email']
    
    if request.method == 'POST': # this is called when they request a billing receipt.
        # code to handle a help desk request
        db = connect()
        command = f"INSERT INTO help_desk(email,subject,message) VALUES('{email}','billing','this user requests a billing receipt.')"
        db.run(command)
        db.commit()
        db.close()
        receipt_confirmation = 'Receipt requested. You will recieve an email with your receipt.'

    return render_template('dashboard.html',
            students=students,
            membership=membership,
            receipt_confirmation=receipt_confirmation)

def change_password(new_password):
    pw_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user_id = flask_login.current_user.id
    user = get_user(user_id)
    print ('Updating password for',user['name'])
    db = connect()
    command = f"UPDATE parents SET pw_hash = '{pw_hash}' WHERE user_id = '{user_id}'"
    db.run(command)
    db.commit()
    db.close()

def change_name(new_name):
    user_id = flask_login.current_user.id
    user = get_user(user_id)
    print ('Updating name for',user['name'])
    db = connect()
    command = f"UPDATE parents SET name = '{new_name}' WHERE user_id = '{user_id}'"
    db.run(command)
    db.commit()
    db.close()

def change_phone(new_phone):
    user_id = flask_login.current_user.id
    user = get_user(user_id)
    print ('Updating phone for',user['name'])
    db = connect()
    command = f"UPDATE parents SET phone = '{new_phone}' WHERE user_id = '{user_id}'"
    db.run(command)
    db.commit()
    db.close()

@app.route('/account', methods=['get','post'])
@flask_login.login_required
def account():
    user_id = flask_login.current_user.id
    user = get_user(user_id)

    if request.method == 'GET':
        return render_template('account.html',user=user)

    account_confirmation = ''
    password_confirmation = ''
    account_warning = ''
    password_warning = ''
    old_password_warning = ''

    if request.method == 'POST':
        form_type = request.form['form-type']
            
        if(form_type == 'change_password'):
            ready = False
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            new_password_confirm = request.form['new_password_confirm']

            if(not logged_in_check_password(old_password)):
                old_password_warning = 'password incorrect!'
            else:
                if(new_password != new_password_confirm):
                    password_warning = 'Passwords do not match!'
                else:
                    if(len(new_password) < 8):
                        password_warning = 'password must be at least 8 characters.'
                    else:
                        if(logged_in_check_password(new_password)):
                            password_warning = 'new password cannot match old password.'
                        else:
                            ready = True
            if(ready):
                change_password(new_password)
                password_confirmation = 'Password sucessfully changed.'

        elif(form_type == 'account_info'):
            new_name = request.form['new_name']
            new_phone = request.form['new_phone']
            old_name = user['name']
            old_phone = user['phone']
            
            print(new_name != old_name)

            ready = False
            if(new_name != old_name):
                if all(x.isalpha() or x.isspace() for x in new_name):
                    if len(new_name) < 30:
                        print('UPDATE NAME')
                        # udpate name
                        change_name(new_name)
                        ready = True
                    else:
                        account_warning = 'Name is 26 characters max.'
                else:
                    account_warning = 'Invalid name'

            if(new_phone != old_phone):
                if all(x.isspace() or x.isdigit() or x == '-' for x in new_phone) and len(new_phone) < 20:
                    # udpate phone number
                    change_phone(new_phone)
                    ready = True
                else:
                    account_warning = 'Invalid phone number'

            if ready:
                account_confirmation = 'Info sucessfully changed.'

        user = get_user(user_id)
        return render_template('account.html',user=user,
                account_warning=account_warning,
                account_confirmation=account_confirmation,
                password_warning=password_warning,
                password_confirmation=password_confirmation,
                old_password_warning=old_password_warning)

@app.route('/helpdesk', methods=['get','post'])
@flask_login.login_required
def helpdesk():
    return render_template('helpdesk.html')

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
