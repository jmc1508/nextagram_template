from flask import Blueprint,  Flask, render_template, request,redirect,url_for,flash,session
from models.user import User
from models.relationship import Relationship
from models.base_model import db
from flask_login import login_user, login_required, current_user




users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates/')


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
@login_required
def show(username):
    # Get user object
    user=User.get_or_none(User.username==username)

    # Get list of images related to this user using the backref
    user_images=user.images
  

    return render_template('users/profile.html', user = user,user_images=user_images)

@users_blueprint.route('/', methods=["POST"])
def index():

    return render_template('home.html')


@users_blueprint.route('/<int:id>/edit', methods=['GET'])
# @login_required
def edit(id):
    user = User.get_or_none(User.id==id)
    
    # Conditions: If user is current_user, then proceed. Else flash message go to to sign-in page

    if current_user==user:
        return render_template('users/edit.html')
    else:
        flash('Error: You are not authorised to edit another profile')
        return render_template('sessions/sign_in.html')

@users_blueprint.route('/<int:id>', methods=['POST'])
def update(id):
    
    username_form=request.form['username']
    email_form=request.form['email']
    password_form=request.form.get('password')

    privacy_form= request.form.get('checkbox')
    
    user= User.get_by_id(id)
    
    user.username=username_form
    user.email=email_form
    # If profile is private and returns something, means user wants to make public
    if user.private == True and privacy_form:
        user.private = False
    else:
        user.private=True

    # If password has been amended, change it
    if password_form:
        user.password=password_form
    # Invoke save() function to do validation
    if user.save():
        flash('User data updated')
        return redirect(url_for('users.edit',id=id))
    else:
        return render_template('/users/edit.html',errors=user.errors)

@users_blueprint.route('/follower/', methods=["POST"])
def new_follower():

    follower_username=request.form['follower_username']
    idol_username = request.form['idol_username']

    # Get ID and add to DB

    follower_id=User.get_or_none(User.username==follower_username)
    idol_id=User.get_or_none(User.username==idol_username)
 
    add_follower=Relationship(follower_id=follower_id, idol_id=idol_id)
    add_follower.save()

    # Get list of followers
    result=Relationship.get_idols(self=add_follower)
    print(result)

    flash(f'You have followed {idol_username}')

    
    return render_template('home.html')


@users_blueprint.route('/test_layout')
def test_layout():


    return render_template('/users/new.html')


    
    
    
