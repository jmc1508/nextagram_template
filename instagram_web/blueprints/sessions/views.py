from app import app
from flask import Blueprint, render_template, Flask, request,redirect,url_for,flash,session
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_user, login_required,logout_user, current_user

from models.user import User
# Google Authorize
from instagram_web.util.google_oauth import google
sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/')



# Moved
@sessions_blueprint.route('/', methods=['GET'])
def new():
    redirect_uri = url_for('sessions.google_login', _external=True)
    return google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google', methods=['GET'])
def google_login():

    # Capture user data from google login
    token = google.authorize_access_token()
    email = google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    result = google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()

    # Check if email is in database
    user = User.get_or_none(User.email==email)

    if user:
        login_user(user)
        flash('Login successful!')
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash('User profile not found.')
        return redirect(url_for('users.new'))
    
    return "PASS"
    

@sessions_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):



    pass

@sessions_blueprint.route('/sign_in', methods=["GET"])
def index():

    return render_template('sessions/sign_in.html')

@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

@sessions_blueprint.route('/sign_in', methods=['POST'])
def check_sign_in():

    # Get username

    user=User.get_or_none(User.username==request.form['username'])
    
    if user:
        password_to_check=request.form['password']
        result=check_password_hash(user.password,password_to_check)

        if result:

            user_login=User.get(User.username==request.form['username'])
            # Flask-login - login the user
            login_user(user_login)
            flash('Logged in successfully')
            # Add in session key
            return redirect(url_for("users.show",username=request.form['username']))
        else:
            flash('Error: Incorrect username or password')
            return render_template('sessions/sign_in.html')
    else:
        flash('Error: Incorrect username or password')

        return render_template('sessions/sign_in.html')

@sessions_blueprint.route('/sign_out')
@login_required
def sign_out():

    logout_user()
    flash("You have successfully logged out!")
    return redirect(url_for('index'))


