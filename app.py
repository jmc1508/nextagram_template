import os
import config
from flask import Flask, render_template, request,redirect,url_for,flash,session
from models.base_model import db
from models.user import User

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


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

