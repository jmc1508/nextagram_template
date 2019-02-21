from flask import Blueprint, render_template


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates/sessions')


# Moved
@users_blueprint.route('/new', methods=['GET'])
def new():
    
    pass


@users_blueprint.route('/', methods=['POST'])
def create():
    pass


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "SESSIONS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
