import os
import config
from flask import Flask, render_template, request,redirect,url_for,flash,session
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_user, login_required,logout_user

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
# Add CSRF
csrf=CSRFProtect(app)
# # Add login manager
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sign_in"
login_manager.login_message ='Testing 123'
login_manager.login_message_category = "info"

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


# Flask-Login user loader
@login_manager.user_loader
def load_user(id):
    # userid=int(userid)
    return User.get_or_none(User.id==id)

# Connect to DB
@app.before_request
def before_request():
    db.connect()

@app.after_request
def after_request(response):
    db.close()
    return response

# View: Index [app.py]
@app.route("/")
def index():

    if 'username' in session:
        print ('User in session')

    return render_template('home.html')

# View: New user [blueprint-users]
# @app.route("/users/new")
# def new_user():

#     return render_template('sign_up.html')

# Create: New user
@app.route("/users/", methods=['POST'])
def create_new_user():

    # Get name,username,email, password
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
 
    # Create new field in User table

    user = User(username=username,email=email,password=password)

    # Create error validation

    if user.save():

        flash('User successfuly signed up')
        return redirect(url_for('sign_in'))
    else:

        return render_template('sign_up.html', errors=user.errors)


# View: User Sign In
@app.route("/sign_in")
def sign_in():

    return render_template('sign_in.html')

# Check: User Sign In
@app.route("/sign_in", methods=['POST'])
def check_sign_in():

    # Get username

    user=User.get_or_none(User.username==request.form['username'])
    
    if user:
        password_to_check=request.form['password']
        result=check_password_hash(user.password,password_to_check)

        if result:

            user_login=User.get(User.username==request.form['username'])
            login_user(user_login)
            flash('Logged in successfully')
            # Add in session key
            # session['username']=request.form['username']
            return redirect(url_for("index"))
        else:
            flash('Error: Incorrect username or password')
            return render_template('sign_in.html')
    else:
        flash('Error: Incorrect username or password')

        return render_template('sign_in.html')



@app.route('/sign_out')
@login_required
def sign_out():
    # remove the username from the session if it's there
    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for('index'))
