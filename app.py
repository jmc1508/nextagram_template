import os
import config
from flask import Flask, render_template, request,redirect,url_for,flash,session
from models.base_model import db

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

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc 

# View: Index [app.py]
# @app.route("/")
# def index():

#     return render_template('home.html')

# Added: Error handler 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

    # Added: Error handler 403
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html')