import os
import config
from flask import Flask, render_template, request,redirect,url_for,flash
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, CSRFError

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)
# Add CSRF
csrf=CSRFProtect(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response

# View: New user
@app.route("/users/new")
def new_user():

    return render_template('sign_up.html'  )


# Create: New user
@app.route("/users/", methods=['POST'])
def create_new_user():

    # Get name,username,email, password
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    # hashed_password=generate_password_hash(password)
 
    # Create new field in User table

    user = User(username=username,email=email,password=password)

    # Create error validation

    if user.save():

        flash('User successfuly signed up')
        return redirect(url_for('new_user'))
    else:

        return render_template('sign_up.html', errors=user.errors)


# View: User Sign In
@app.route("/sign_in")
def sign_in():


    return render_template('sign_in.html')

# Check: User Sign In
@app.route("/sign_in", methods=['POST'])
def check_sign_in():

    get_username=request.form['username']
    
    # query = User.get(User.id).where(User.username==get_username)




    return redirect(url_for("sign_in"))
