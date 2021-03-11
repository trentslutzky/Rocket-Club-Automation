from flask import Flask, render_template, request, redirect
from flask_bcrypt import Bcrypt
import flask_login, flask
import os,sys
import pgTool as pgtool
import secret
import pg8000
import rcCerts as rccerts

sys.path.insert(1, os.path.join(sys.path[0], '..'))

app = Flask(__name__)
app.secret_key = secret.app_secret
bcrypt = Bcrypt(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

import datetime
from datetime import datetime
from datetime import date


##### DATABASE FUNCTIONS     ########

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

def get_user(username):
    db = connect()
    ps = qprep(db,"SELECT username,pw_hash,role FROM admin_dashboard_logins WHERE username=:u")
    result = ps.run(u=username)
    if(result):
        return {
                'username':result[0][0],
                'password':result[0][1],
                'role':result[0][2],
                }
    else:
        return None

###### STUFF FOR ADMIN-SITE  #########
class User():
    role = ''

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
    user_get = get_user(username)
    if(not user_get):
        return
    user = User()
    user.role = user_get['role']
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    print('request_loader')
    username = request.form.get('username')
    user_get = get_user(username)
    if(not user_get):
        return
    user = User()
    user.id = username
    user.role = user_get['role']
    if(bcrypt.check_password_hash(
        user_get['password'],request.form['password'])
        ):
        return user
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    return flask.redirect(flask.url_for('dashboard'))

@app.route('/dashboard')
@flask_login.login_required
def dashboard():
    username = flask_login.current_user.get_id() 
    role = flask_login.current_user.get_role() 
    print(username,role)
    return render_template('admin-dashboard.html',
            username=username,
            role=role)

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
            return redirect('dashboard')

@app.route('/add-member', methods=['GET','POST'])
@flask_login.login_required
def add_member():
    num = 30
    confirmation = ''
    warning = ''
    teams = pgtool.get_teams()
    defaut_grad_date = 'April 2023'
    if flask.request.method == 'GET':
        next_member_id = pgtool.get_next_member_id()
        recent_members = pgtool.get_recent_members(num)
        return render_template('add-member.html',
                teams=teams,
                next_member_id=next_member_id,
                recent_members=recent_members,
                num = num,
                defaut_grad_date = defaut_grad_date
                )

    elif flask.request.method == 'POST':
        current_id = request.form['member_id_input']
        name = request.form['name']
        division = request.form['division']
        team = request.form['team']
        grad_date = request.form['grad_date']
        parent_name = request.form['parent_name']
        parent_email = request.form['parent_email']
        parent_phone = request.form['parent_phone']
        cost = request.form['cost']
        scholarship = request.form['scholarship']

        member_exists = pgtool.test_member_id(current_id)

        if(name == ''):
            warning = 'Invalid Name!'
        elif(division == ''):
            warning = 'Please enter a division!'
        elif(team == ''):
            warning = 'Please select a team!'
        elif(member_exists != 0):
            warning = 'Member ID exists. Please enter a different member ID.'
        else:
            name = name.title()
            confirmation = 'Member Added ' + str(current_id) + ' ' + name
            pgtool.add_new_member(current_id,name,division,team,grad_date)
            pgtool.add_parent(current_id,parent_name,parent_email,parent_phone,cost,scholarship)

        recent_members = pgtool.get_recent_members(num)
        next_member_id = pgtool.get_next_member_id()
        return render_template('add-member.html',
                teams=teams,
                next_member_id=next_member_id,
                recent_members=recent_members,
                num = num,
                confirmation = confirmation,
                defaut_grad_date = defaut_grad_date,
                warning = warning
                )

@app.route('/edit-member', methods=['GET','POST'])
@flask_login.login_required
def edit_member():
    search_warning = ''
    if flask.request.method == 'GET':
        return render_template('edit-member.html',ready=False)

    elif flask.request.method == 'POST':
        query = request.form['member-query']
        query = query.replace("'",'')
        query = query.replace('"','')
        query = query.replace('!','')
        query = query.replace('\\','')
        query = query.replace(';','')
        query = query.replace(':','')
        query = query.replace('<','')
        query = query.replace('&','')
        query = query.replace('(','')
        query = query.replace(')','')
        query = query.replace(' ','|')
        results = pgtool.search_members(query)
        if(len(results) == 0):
            search_warning = 'No Results'
        return render_template('edit-member.html',
                ready=True,
                results = results,
                search_warning = search_warning)

@app.route('/class-rf', methods=['GET','POST'])
@flask_login.login_required
def class_rf():
    today = date.today()
    dt = pgtool.get_date_today()
    date_string = dt.strftime('%B %-d')
    teams = pgtool.get_teams()
    if flask.request.method == 'GET':
        return render_template('class-rf.html', teams=teams,ready=False)

    if flask.request.method == 'POST':
        form_type = request.form['form_type']
        team = request.form['team']
        team_members = pgtool.get_team_members(team)

        if form_type == 'team_select':
            return render_template('class-rf.html', 
                    date=date_string,
                    team=team,
                    team_members=team_members,
                    ready=True)

        elif form_type == 'rf-add':
            print('class-rf-add',team)
            attended = request.form.getlist('attendance')
            print('attended:',attended)
            pgtool.update_attendance(team,attended)
            amount_changed = 0

            for line in request.form:
                if line != 'form_type' and line != 'team' and line != 'attendance':
                    amount = request.form[line]
                    line_split = line.split('!')
                    member_uuid = line_split[0]
                    subtype = line_split[1]
                    t_type = 'class'
                    current_amount = 0
                    amount = amount.replace(' ','')
                    if amount == '':
                        amount = 0

                    for member in team_members:
                        if str(member['uuid']) == member_uuid:
                            if member[subtype]:
                                current_amount = member[subtype]

                    if int(amount) != current_amount:
                        amount_changed = amount_changed + 1
                        print(member_uuid,t_type,subtype,amount)
                        pgtool.update_class_category(member_uuid,subtype,amount)

            team_members = pgtool.get_team_members(team)
            current_time = pgtool.get_current_time()
            return render_template('class-rf.html', 
                date=date_string,
                team=team,
                team_members=team_members,
                confirmation=f'Updated {current_time}',
                ready=True)


@app.route('/member-detail', methods=['GET','POST'])
@flask_login.login_required
def member_detail():
    teams = pgtool.get_teams()
    if flask.request.method == 'GET':
        member_uuid = request.args.get('m_uuid','')
        member = pgtool.get_member_info_uuid(member_uuid)
        rf_transactions = pgtool.get_recent_rf_transactions(member_uuid)
        total_rf = pgtool.get_member_total_uuid(member_uuid)
        #NEED TO ADD PARENT FUNCTIONALITY
        parent = {'name':'', 'email':'', 'phone':''}
        return render_template('member-detail.html',
                member=member,
                rf_transactions=rf_transactions,
                total_rf=total_rf,
                member_uuid=member_uuid,
                parent=parent,
                role=flask_login.current_user.get_role(),
                teams=teams
                )

    if flask.request.method == 'POST':
        # get info needed to render page
        member_uuid = request.form['member_uuid']

        # get data from change-info form
        new_member_id = request.form['member_id']
        new_name = request.form['name']
        new_division = request.form['division']
        new_team = request.form['team']
        new_grad_date = request.form['grad_date']

        # send new data to the database
        update = pgtool.update_member_info(member_uuid,
                new_member_id,new_name,new_team,new_division,new_grad_date)

        # render page
        warning = '';
        confirmation = '';
        if(update == 2):
            warning = 'Member ID Exists! Try again.'
        if(update == 0):
            confirmation = 'Updated!'
        if(update == 1):
            confirmation = 'You didn\'t change anything...'

        member = pgtool.get_member_info_uuid(member_uuid)
        rf_transactions = pgtool.get_recent_rf_transactions(member_uuid)
        total_rf = pgtool.get_member_total_uuid(member_uuid)

        #NEED TO ADD PARENT FUNCTIONALITY
        parent = {'name':'', 'email':'', 'phone':''}

        return render_template('member-detail.html',
                member=member,
                rf_transactions=rf_transactions,
                total_rf=total_rf,
                member_uuid=member_uuid,
                warning=warning,
                teams=teams,
                confirmation=confirmation,
                role=flask_login.current_user.get_role(),
                parent=parent
                )

@app.route('/member-detail-view', methods=['GET'])
@flask_login.login_required
def member_detail_view():
    teams = pgtool.get_teams()
    if flask.request.method == 'GET':
        member_uuid = request.args.get('m_uuid','')
        member = pgtool.get_member_info_uuid(member_uuid)
        rf_transactions = pgtool.get_recent_rf_transactions(member_uuid)
        total_rf = pgtool.get_member_total_uuid(member_uuid)
        return render_template('member-detail-view.html',
                member=member,
                rf_transactions=rf_transactions,
                total_rf=total_rf,
                member_uuid=member_uuid,
                teams=teams
                )

@app.route('/add-rf', methods=['GET','POST'])
@flask_login.login_required
def add_rf():
    if flask.request.method == 'GET':
        types = pgtool.get_types()
        return render_template('add-rf.html',
                types = types)

    elif flask.request.method == 'POST':

        member_id = request.form['member_id']
        mtype = request.form['type']
        amount = request.form['amount']

        name = pgtool.get_member_name(int(member_id))

        if(name):
            confirm = str(amount) + ' RF added for ' + name
            pgtool.add_rf_transaction(member_id,mtype,'',amount)
        else:
            confirm = 'INVALID MEMBER ID. Please try again'


        print('Adding RF',member_id,mtype,name)
        return render_template('add-rf.html',
                types = pgtool.get_types(),
                confirm = confirm)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('login.html', warning = 'logged out')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html',warning = 'please log in.')

############## CERT SITE #############

def get_cert_page(member_id):
    output = []
    entre_certs = rccerts.get_certs('entre')
    robotics_certs = rccerts.get_certs('robotics')
    tech_certs = rccerts.get_certs('tech')

    # get the member's current certs
    member_current_certs = rccerts.get_member_certs(member_id)

    # initialize empty arrays for current certs
    entre_certs_current = []
    robotics_certs_current = []
    tech_certs_current = []

    # initialize arays for non-current certs
    entre_certs_noncurrent = []
    robotics_certs_noncurrent = []
    tech_certs_noncurrent = []

    # go through the open certs and remove the current ones.
    for c in entre_certs:
        old = c[0]
        current = False

        for a in member_current_certs:
            if old == a[0]:
                current = True

        if current:
            entre_certs_current.append(c)
        else:
            entre_certs_noncurrent.append(c)

    for c in robotics_certs:
        old = c[0]
        current = False

        for a in member_current_certs:
            if old == a[0]:
                current = True

        if current:
            robotics_certs_current.append(c)
        else:
            robotics_certs_noncurrent.append(c)

    for c in tech_certs:
        old = c[0]
        current = False

        for a in member_current_certs:
            if old == a[0]:
                current = True

        if current:
            tech_certs_current.append(c)
        else:
            tech_certs_noncurrent.append(c)

    output.append(entre_certs_current)
    output.append(entre_certs_noncurrent)
    output.append(robotics_certs_current)
    output.append(robotics_certs_noncurrent)
    output.append(tech_certs_current)
    output.append(tech_certs_noncurrent)

    return output

@app.route('/certs', methods=['GET','POST'])
@flask_login.login_required
def update_certs():
    if flask.request.method == 'GET':
        member_id_get = request.args.get('member_id_get') 
        if(member_id_get):
            member_name = pgtool.get_member_name(int(member_id_get))
            if(member_name != None):
                data = get_cert_page(member_id_get)
                return render_template('update_certs.html',ready=True,
                        submit_prompt = 'Select/Deselect certifications then press submit.',
                        entre_certs_current = data[0],
                        entre_certs_noncurrent = data[1],
                        robotics_certs_current = data[2],
                        robotics_certs_noncurrent = data[3],
                        tech_certs_current = data[4],
                        tech_certs_noncurrent = data[5],
                        member_name = member_name,
                        member_id = member_id_get)
        else:
            return render_template('update_certs.html',ready=False)

    if flask.request.method == 'POST':
        member_id_get = request.args.get('member_id_get') 
        certs = request.form.getlist('cert-check-box')
        member_name = pgtool.get_member_name(int(member_id_get))
        submit_confirm = ''
        submit_warning = ''

        # update certs in database:
        try:
            rccerts.update_certs(member_id_get,certs)
            submit_confirm = ('Updated certifications for ' 
                    + str(member_name) + '!')
        except AttributeError as err:
            print('ERROR:',err)
            submit_warning = 'Error occured. Please contact tech support!'
        member_name = pgtool.get_member_name(int(member_id_get))

        # generate a new cert page with the updated stuff
        data = get_cert_page(member_id_get)
        return render_template('update_certs.html',ready=True,
                submit_warning = submit_warning,
                submit_confirm = submit_confirm,
                entre_certs_current = data[0],
                entre_certs_noncurrent = data[1],
                robotics_certs_current = data[2],
                robotics_certs_noncurrent = data[3],
                tech_certs_current = data[4],
                tech_certs_noncurrent = data[5],
                member_name = member_name,
                member_id = member_id_get)

        ######################################

@app.route('/my-rf', methods=['GET', 'POST'])
def my_rf():
    return render_template('gate.html',
            warning = '')

@app.route('/')
def gate_loading():
    print('get_loading')
    return render_template('gate.html',
            warning = 'LOADING...')

@app.route('/rcl_attendance', methods=['GET', 'POST'])
def rcl_attendance():
    date = pgtool.get_date_today()
    if flask.request.method == 'GET':
        return render_template('rcl_attendance.html',date=date,get=True)
    
    if flask.request.method == 'POST':
        member_id = flask.request.form['member_id']
        code_input = flask.request.form['code']
        print(member_id,code_input)
        attendance_check = pgtool.check_code(member_id,code_input)
        if(attendance_check):
            return render_template('rcl_attendance.html',
                    date=date,get=False,
                    confirmation='Attendance confirmed for Trent Slutzky'
                    )
        else:
            return render_template('rcl_attendance.html',
                    date=date,get=True,
                    warning='Invalid Code!')
    

@app.route('/stats', methods=['GET', 'POST'])
def show_stats():
    if request.method == 'POST':
        
        #Get member name, team, division
        member_id = request.form['member-id']
       
        test = pgtool.get_member_uuid(member_id)

        if test == -1:
            return render_template('gate.html',
                warning = 'Invalid member id!')
        else:
            gate_loading()
            # Member info from pgtool
            member_info = pgtool.get_member_info(member_id)
            # Member total RF
            member_rf = pgtool.get_member_total(member_id)
            # Member Virtual Mission RF
            vm_total = pgtool.get_vm_rf(member_id)
            # categories for vm categories
            vm_categories_rf = pgtool.get_vm_rf_categories(member_id)
            # VMs completed
            vm_completions = pgtool.get_member_vms_completed(member_id)
            # RCL RF
            rcl_rf = pgtool.get_member_rcl_rf(member_id)
            # MISC RF
            misc_rf = pgtool.get_member_misc_rf(member_id)
            
            member_rf =str(format(int(member_rf),','))

            data = get_cert_page(member_id)

            return render_template('member_dashboard.html', 
            name = member_info[0], 
            division = member_info[1], 
            team = member_info[2], 
            rf_total = member_rf,
            entre_certs_current = data[0],
            entre_certs_noncurrent = data[1],
            robotics_certs_current = data[2],
            robotics_certs_noncurrent = data[3],
            tech_certs_current = data[4],
            tech_certs_noncurrent = data[5],
            grad_date = member_info[4],
            phone = '(201) 292-3565',
            email = 'admin@rocketclub.com',
            website = 'rocketclub.com',
            #rf_vm = vm_total,
            #robotics_rf = vm_categories_rf[0],
            #coding_rf = vm_categories_rf[1],
            #engineering_rf = vm_categories_rf[2],
            #entrepreneurship_rf = vm_categories_rf[3],
            #past_rf = vm_categories_rf[4],
            #extra_credit_rf = vm_categories_rf[5],
            #n_robotics = vm_completions[0],
            #n_coding = vm_completions[1],
            #n_python = vm_completions[2],
            #n_robotics_1 = vm_completions[3],
            #n_engineering = 0,
            #n_entre = vm_completions[4],
            #rf_rcl_attendance = rcl_rf[1],
            #rf_trivia = rcl_rf[2],
            #rf_won = misc_rf[2],
            #rf_rcl_total = rcl_rf[0],
            #rf_boost = misc_rf[0],
            #rf_rcgt = misc_rf[1],
            #rf_parents = rcl_rf[3],
            #rf_class = misc_rf[3],
            #rf_launchpad = rcl_rf[4],
            #rf_tech_tuesday = rcl_rf[5]
            )

@app.route('/resume/<string:m_id>')
def resume(m_id):
    member_id = int(m_id)
    # Member info from pgtool
    member_info = pgtool.get_member_info(member_id)
    # Member total RF
    member_rf = pgtool.get_member_total(member_id)
    # Member Virtual Mission RF
    vm_total = pgtool.get_vm_rf(member_id)
    # categories for vm categories
    vm_categories_rf = pgtool.get_vm_rf_categories(member_id)
    # VMs completed
    vm_completions = pgtool.get_member_vms_completed(member_id)
    # RCL RF
    rcl_rf = pgtool.get_member_rcl_rf(member_id)
    # MISC RF
    misc_rf = pgtool.get_member_misc_rf(member_id)
    
    member_rf =str(format(int(member_rf),','))

    data = get_cert_page(member_id)

    member_info[1] = member_info[1].replace('Division ','')

    grad_date = 'June 2022'
    if member_id in members_feb2021:
        grad_date = 'Feb 2021'

    return render_template('resume_template.html', 
        name = member_info[0], 
        division = member_info[1], 
        team = member_info[2], 
        rf_total = member_rf,
        entre_certs_current = data[0],
        entre_certs_noncurrent = data[1],
        robotics_certs_current = data[2],
        robotics_certs_noncurrent = data[3],
        tech_certs_current = data[4],
        tech_certs_noncurrent = data[5],
        grad_date = grad_date,
        phone = '(201) 292-3565',
        email = 'admin@rocketclub.com',
        website = 'rocketclub.com',
        #rf_vm = vm_total,
        #robotics_rf = vm_categories_rf[0],
        #coding_rf = vm_categories_rf[1],
        #engineering_rf = vm_categories_rf[2],
        #entrepreneurship_rf = vm_categories_rf[3],
        #past_rf = vm_categories_rf[4],
        #extra_credit_rf = vm_categories_rf[5],
        #n_robotics = vm_completions[0],
        #n_coding = vm_completions[1],
        #n_python = vm_completions[2],
        #n_robotics_1 = vm_completions[3],
        #n_engineering = 0,
        #n_entre = vm_completions[4],
        #rf_rcl_attendance = rcl_rf[1],
        #rf_trivia = rcl_rf[2],
        #rf_won = misc_rf[2],
        #rf_rcl_total = rcl_rf[0],
        #rf_boost = misc_rf[0],
        #rf_rcgt = misc_rf[1],
        #rf_parents = rcl_rf[3],
        #rf_class = misc_rf[3],
        #rf_launchpad = rcl_rf[4],
        #rf_tech_tuesday = rcl_rf[5]
        )

@app.route('/team/<string:team_name>')
def show_team_stats(team_name):
    print('Loading information for team: '+team_name)
    
    member_names = pgtool.get_team_members(team_name)
    num_members = len(member_names)
    instructor = pgtool.get_instructor(team_name)
    
    weekly_missions = pgtool.get_weekly_missions()
    weekly_completions = pgtool.get_current_weekly_missions_completed(team_name)
    vms_completed = pgtool.get_team_vms_completed(team_name)

    return render_template('team_stats.html',
            team_name=team_name,
            instructor_name=instructor,
            member_names=member_names,
            num_members=num_members,
            
            num_robotics_overview=vms_completed[0],
            robotics_total = int(num_members) * 30,
            robotics_percent = int(vms_completed[0])/(int(num_members)*30)*100,

            num_coding_overview=vms_completed[1],
            coding_overview_total = int(num_members) * 30,
            coding_percent = int(vms_completed[1])/(int(num_members)*30)*100,
            
            num_python_1 = vms_completed[2],
            python_total = int(num_members) * 50,
            python_percent = int(vms_completed[2])/(int(num_members)*30)*100,
            
            num_robotics_1 = vms_completed[3],
            robotics_1_total = int(num_members) * 30,
            robotics_1_percent = int(vms_completed[3])/(int(num_members)*30)*100,
            
            num_entre_1 = vms_completed[4],
            entre_total = int(num_members) * 15,
            entre_percent = int(vms_completed[4])/(int(num_members)*30)*100,
            
            num_1 = weekly_completions[0],
            num_1_percent = int(weekly_completions[0])/int(num_members)*100,
            num_2 = weekly_completions[1],
            num_2_percent = int(weekly_completions[1])/int(num_members)*100,

            mission_1 = weekly_missions[0],
            mission_2 = weekly_missions[1]
            )

@app.route('/leaderboard')
def show_leaderboard():
    #get top ten table
    team_standings = pgtool.get_team_standings()
    division_standings = pgtool.get_division_standings()
    legacy_leaders = pgtool.get_legacy_leaders()
    trivia_leaders = pgtool.get_trivia_leaders()
    parents_night_leaders = pgtool.get_parents_night_leaders()

    return render_template('test_leaderboard.html',
                team_standings=team_standings,
                division_standings=division_standings,
                legacy_leaders=legacy_leaders,
                trivia_leaders=trivia_leaders,
                parents_night_leaders=parents_night_leaders
            )

def add_user(username,password,role):
    db = connect()
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    COMMAND = f"INSERT INTO admin_dashboard_logins(username,pw_hash,role) VALUES('{username}','{pw_hash}','{role}')"
    db.run(COMMAND)
    db.commit()
    db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')













