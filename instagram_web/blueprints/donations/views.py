from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash

from werkzeug import secure_filename

from models.user import User
from models.image import Image
from models.donation import Donation
from flask_login import login_required, current_user

# Braintree import
from instagram_web.util.braintree import generate_client_token, gateway
# Sendgrid impot
from instagram_web.util.sendgrid import send_donation_email

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates/')


@donations_blueprint.route('/new/<int:image_id>', methods=['POST'])
def new(image_id):
    # Create client_token - needed to open donation form
    client_token = generate_client_token()
    donor_id = request.form['donor']
    receiver_id = request.form['receiver']

    receiver = User.get_by_id(receiver_id)
    receiver_username = receiver.username

    return render_template('donations/donate.html', client_token=client_token, image_id=image_id, donor_id=donor_id, receiver_username=receiver_username)


@donations_blueprint.route('/<int:image_id>', methods=['POST'])
def create(image_id):

    # Get form info
    payment_method_nonce = request.form['payment_method_nonce']
    amount = request.form['amount']
    donor_id = request.form['donor_id']
    receiver_username = request.form['receiver_username']
    image_id = image_id

    # Get donor_id details
    donor=User.get_by_id(donor_id)
    sender= donor.email

    # Create a transactionr
    result = gateway.transaction.sale({
        # Need to amend amount
        'amount': amount,
        'payment_method_nonce': payment_method_nonce,
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        transaction_id = result.transaction.id
        donation = Donation(image=image_id, amount=amount, donor=donor_id,
                            currency="USD", transaction_id=result.transaction.id)

        if donation.save():
            flash(f'Your {result.transaction.currency_iso_code}{amount} donation to {receiver_username} was successful. The receipt number is {result.transaction.id}')
            email=send_donation_email(amount=amount, receiver="bobteo1956@gmail.com", sender = sender)
            return redirect(url_for('donations.show', transaction_id=transaction_id))
        else:
            flash('Your donation could not save to the database. Data validation failed?')
            return redirect(url_for('users.show', username=current_user.username))

    else:

        flash(f'Donation failed: {result.transaction.status}')
        return redirect(url_for('users.show', username=current_user.username))


# Show checkout
@donations_blueprint.route('/success/<transaction_id>', methods=["GET"])
def show(transaction_id):

    # flash('You have successfully made a donation.')

    # donor_id=current_user.id
    return redirect(url_for('users.show', username=current_user.username))


@donations_blueprint.route('/', methods=["GET"])
def index():

    pass


@donations_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@donations_blueprint.route('/<int:id>', methods=['POST'])
def update(id):

    pass
