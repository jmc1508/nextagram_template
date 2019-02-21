from flask import Blueprint,  Flask, render_template, request,redirect,url_for,flash,session
from models.user import User
from models.base_model import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_user, login_required,logout_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/')


# Moved
@users_blueprint.route('/new', methods=['GET'])
def new():
    
    return render_template('users/sign_up.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    # Get name,username,email, password
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
 
    # Create new field in User table

    user = User(username=username,email=email,password=password)

    # Create error validation

    if user.save():

        flash('User successfuly signed up')
        return redirect(url_for('sessions.index'))
    else:

        return render_template('users/sign_up.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
