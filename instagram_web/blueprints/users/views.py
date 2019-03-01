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
    
    # If current_user is a follower of page's idol, toggle Unfollow button
    
    
    # Object of profile page user
    user=User.get_or_none(User.username==username)

    result = Relationship.get_or_none(current_user.id==Relationship.follower_id, user.id==Relationship.idol_id)
    
    if result:
        toggle_unfollow=True
    else:
        toggle_unfollow=False

    
    # Get relationship objects
    relationship_following=Relationship.get_or_none(Relationship.follower_id==user.id)  #To see who I am following, look in the follower_id column
    relationship_followers=Relationship.get_or_none(Relationship.idol_id==user.id)
    
    # Get list of images related to this user using the backref
    user_images=user.images
 
    # Get count of who this user is following

    if relationship_following:
        following=relationship_following.count_idols()
        # list_following=relationship_following.get_idols()
    else:
        following=0
        
    if relationship_followers:
        followers=relationship_followers.count_fans()
    else:
        followers=0
    
    
    # print(list_following)
    
    return render_template('users/profile.html', user = user,followers=followers, following=following, toggle_unfollow=toggle_unfollow)

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
def follow_user():

    follower_username=request.form['follower_username']
    idol_username = request.form['idol_username']

    # Get ID and add to DB

    follower_id=User.get_or_none(User.username==follower_username)
    idol_id=User.get_or_none(User.username==idol_username)
 
    add_follower=Relationship(follower_id=follower_id, idol_id=idol_id)
    add_follower.save()

    flash(f'You have followed {idol_username}')

    return render_template('home.html')

@users_blueprint.route('/unfollow/', methods=["POST"])
def unfollow_user():


    follower_username=request.form['follower_username']
    idol_username = request.form['idol_username']

    idol_id=User.get(User.username==idol_username)

    result=Relationship.get_or_none(current_user.id==Relationship.follower_id, Relationship.idol_id==idol_id.id)
    
    # Delete record where Relationship.id = result
    query = Relationship.get_by_id(result)
    query.delete_instance()

    flash(f'You have unfollowed {idol_username}')

    return render_template('home.html')

@users_blueprint.route('/test_layout')
def test_layout():


    return render_template('/users/new.html')


    
    
    
