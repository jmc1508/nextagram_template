import os
import config
from flask import Flask, render_template, request,redirect,url_for,flash
from models.base_model import db
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

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

# View: User sign in
@app.route("/users/new")
def new_user():

    return render_template('sign_up.html',   )

# Create: User sign in
@app.route("/users", methods=['POST'])
def create_new_user():

    # Get name,username,email, password
    username=request.form['username']
    email=request.form['email']
    password=request.form['password']

    print('Username is ', username)
    print('Email is ', email)
    print('Password is ', password)

    return redirect(url_for('new_user'))