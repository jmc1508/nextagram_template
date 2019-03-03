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
    
    # Object of profile page user
    user=User.get_or_none(User.username==username)
    
    # Validation to toggle buttons
    follower_check = Relationship.get_or_none(current_user.id==Relationship.follower_id, user.id==Relationship.idol_id)
    user_authenticated=current_user.is_authenticated
    
    # Toggle "Follow" or "Unfollow" and "Request Pending"
    if follower_check:
        toggle_unfollow=True
        if follower_check.approve==False:
            toggle_request_btn=True
        else:
            toggle_request_btn=False
    else:
        toggle_unfollow=False
        toggle_request_btn=False
    
    # Get relationship objects - gets only one instance
    relationship_following=Relationship.get_or_none(Relationship.follower_id==user.id)  #To see who I am following, look in the follower_id column
    relationship_followers=Relationship.get_or_none(Relationship.idol_id==user.id)

    # Get count of who this user is following

    if relationship_following:
        following=relationship_following.count_idols()
    else:
        following=0
        
    if relationship_followers:
        followers=relationship_followers.count_fans()
    else:
        followers=0

    # Private vs. Public Profile
    relationship_obj=Relationship.get_or_none(Relationship.follower_id==current_user.id, Relationship.idol_id==user.id)

    if relationship_obj and relationship_obj.approve==True:
        toggle_view=True
        # Display full page
    elif relationship_obj and relationship_obj.approve==False:
        # Not approved yet - display private profile
        toggle_view=False
    elif relationship_obj==None and user.private==False:
        #Not following, but public profile
        toggle_view = True
        print('Not following and public page')

    elif relationship_obj==None and user.private==True:
        #Not following and private page
        toggle_view=False
        print('Not following and private page')
    else:
        toggle_view=False
    
    # Get list of who current user is following
    list_following = User.select().join(Relationship, on=Relationship.idol_id).where(Relationship.follower_id==user.id, Relationship.approve==True)
    list_follower=User.select().join(Relationship, on=Relationship.follower_id).where(Relationship.idol_id==user.id)
    
    return render_template('users/profile.html', user = user,followers=followers, following=following, toggle_unfollow=toggle_unfollow,user_authenticated=user_authenticated,toggle_request_btn=toggle_request_btn, toggle_view=toggle_view,list_following=list_following, list_follower=list_follower)

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
@login_required
def follow_user():

    follower_username=request.form['follower_username']
    idol_username = request.form['idol_username']

    # Get ID and add to DB

    follower_id=User.get_or_none(User.username==follower_username)
    idol_id=User.get_or_none(User.username==idol_username)
    
    
    # If user profile = Public, then add follower and approve
    if idol_id.private==False:
        add_follower=Relationship(follower_id=follower_id, idol_id=idol_id, approve=True)
        flash(f'You have followed {idol_username}')
    # If user profile = Private, then add follower but don't approve
    elif idol_id.private==True:
        add_follower=Relationship(follower_id=follower_id, idol_id=idol_id, approve=False)
        flash(f'A friend request has been sent to {idol_username}')

    add_follower.save()

    return render_template('home.html')

@users_blueprint.route('/unfollow/', methods=["POST"])
@login_required
def unfollow_user():


    follower_username=request.form['follower_username']
    idol_username = request.form['idol_username']
    request_type= request.form['request_type']
    
    idol_id=User.get(User.username==idol_username)

    result=Relationship.get_or_none(current_user.id==Relationship.follower_id, Relationship.idol_id==idol_id.id)
    
    # Delete record where Relationship.id = result
    query = Relationship.get_by_id(result)
    query.delete_instance()

    if request_type=='cancel_request':
        flash(f'You have cancelled your request to follow {idol_username}')
    elif request_type=='unfollower_user':
        flash(f'You have unfollowed {idol_username}')

    return render_template('home.html')

@users_blueprint.route('/requests/')
@login_required
def user_requests():

    # Query - users followed by current_user
    idols = User.select().join(Relationship, on=Relationship.idol_id).where(Relationship.follower_id==current_user.id, Relationship.approve==False)
    fans = User.select().join(Relationship, on=Relationship.follower_id).where(Relationship.idol_id==current_user.id, Relationship.approve==False)
    
    return render_template('/users/requests.html', idols=idols, fans = fans)

@users_blueprint.route('/handle_request/',methods =['POST'])
@login_required
def handle_request():

    follower_id=request.form['follower_id']
    idol_id = request.form['idol_id']
    follower=User.get_by_id(follower_id)

    request_type=request.form['request_type']
    # Change privacy setting
    if request_type=='accept_request':
        query = Relationship.get_or_none(Relationship.follower_id==follower_id, Relationship.idol_id==idol_id)
        approve_request=Relationship.update(approve=True).where(Relationship.id==query)
        approve_request.execute()
        flash(f"You have approved {follower.username}'s request.")
        return render_template('home.html')

    elif request_type=='cancel_request':

        breakpoint()
        result=Relationship.get_or_none(Relationship.follower_id==follower_id, Relationship.idol_id==idol_id)
        delete_request=result.delete_instance()
        flash(f"You have denied {follower.username}'s request. ")
        return render_template('home.html')



    
    
    
