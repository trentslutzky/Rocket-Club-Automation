import flask, flask_login
from flask import render_template

app = flask.Flask(__name__)
app.secret_key = 'armstrong1234'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'RocketClubAdmin': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[username]['password']

    return user

@app.route('/')
def home():
    return 'HOMEPAGE'

@app.route('/admin')
def admin():
    return flask.redirect(flask.url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    username = flask.request.form['username']

    if username != 'RocketClubAdmin':
        return render_template('login.html', warning = 'Invalid Login - Try again.')

    elif flask.request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))

    return render_template('login.html', warning = 'Invalid Login - Try again.')

@app.route('/dashboard')
@flask_login.login_required
def protected():
    return render_template('admin-dashboard.html')

@app.route('/add-member')
@flask_login.login_required
def addMember():
    return 'ADD MEMBER'

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('login.html', warning = 'logged out')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('restricted.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
