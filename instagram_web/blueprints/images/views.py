from flask import Blueprint, render_template


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates/')


# Moved
@images_blueprint.route('/new', methods=['GET'])
def new():
    
    pass


@images_blueprint.route('/', methods=['POST'])
def create():
    pass


@images_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass

#Moved
@images_blueprint.route('/', methods=["GET"])
def index():

    pass

@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
