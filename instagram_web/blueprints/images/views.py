from flask import Blueprint, render_template, request, redirect
# from helpers import *    #Where to put this?

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates/')


@images_blueprint.route('/new', methods=['GET'])
def new():
    
    pass


@images_blueprint.route('/', methods=['POST'])
def create():
    pass


@images_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass

@images_blueprint.route('/', methods=["GET"])
def index():

    pass

@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


# From users-> edit.html -> profile image upload
@images_blueprint.route('/<id>', methods=['POST'])
def update(id):

    

    return "PASS"