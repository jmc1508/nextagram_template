from flask import Blueprint, render_template, Flask, request,redirect,url_for,flash,session
from models.base_model import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_login import LoginManager, login_user, login_required,logout_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/')


# Moved
@sessions_blueprint.route('/new', methods=['GET'])
def new():
    
    pass


@sessions_blueprint.route('/', methods=['POST'])
def create():
    pass


@sessions_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass

#Moved successfully
@sessions_blueprint.route('/sign_in', methods=["GET"])
def index():

    return render_template('sessions/sign_in.html')

@sessions_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@sessions_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
