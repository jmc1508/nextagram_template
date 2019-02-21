from flask import Blueprint,  Flask, render_template, request,redirect,url_for,flash,session
from models.user import User
from models.base_model import db
from flask_login import login_user, login_required, current_user


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
        # Before redirect, login the user using Flask-Login
        login_user(user)
        return redirect(url_for('users.show',username=username))
    else:

        return render_template('users/sign_up.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    print('YOU ARE HERE')
    return render_template('home.html')

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)
    
    current_id=User.get(User.id==id).id

    # Conditions: If user is current_user, then proceed

    if current_user==user:
        print("Hooray")
        username=User.get_by_id(id).username
        email=User.get_by_id(id).email
        return render_template('users/edit.html',username=username,email=email, id=id)
        # pass
    else:

        pass

@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    # print('pass')
    username=User.get_by_id(id).username
    flash("Information Updated!")
    return redirect(url_for('users.show', username=username))
