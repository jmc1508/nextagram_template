from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash

from werkzeug import secure_filename

from models.user import User
from models.image import Image
from flask_login import login_required, current_user


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates/')


@donations_blueprint.route('/new', methods=['GET'])
def new():
    
    pass


@donations_blueprint.route('/', methods=['POST'])
def create():
    pass


@donations_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass

@donations_blueprint.route('/', methods=["GET"])
def index():

    pass

@donations_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@donations_blueprint.route('/<int:id>', methods=['POST'])
def update(id):

    pass


    
 
