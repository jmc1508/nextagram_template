from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash

from werkzeug import secure_filename

from models.user import User
from models.image import Image
from flask_login import login_required, current_user

from instagram_web.util.braintree import generate_client_token


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates/')


@donations_blueprint.route('/new/<int:image_id>', methods=['POST'])
def new(image_id):
    
    client_token=generate_client_token()
    donor_id=request.form['donor']

    return render_template('donations/donate.html', client_token=client_token, image_id=image_id, donor_id=donor_id)


@donations_blueprint.route('/<int:image_id>', methods=['POST'])
def create(image_id):
    
    # Get form info
    payment_method_nonce=request.form['payment_method_nonce']
    amount = request.form['amount']
    donor_id=request.form['donor']

    # Store in the database
    breakpoint()
    return "HELLO"


@donations_blueprint.route('/<int:image_id>', methods=["GET"])
def show():
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


    
 
