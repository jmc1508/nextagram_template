import braintree
from app import app

# Braintree: Authentication process
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config['BRAINTREE_MERCHANT_ID'],
        public_key=app.config['BRAINTREE_PUBLIC_KEY'],
        private_key=app.config['BRAINTREE_PRIVATE_KEY']
    )
)

# Braintree - generate a client token
def generate_client_token():
  return gateway.client_token.generate()

# Braintree - receive a payment method nonce from your client once a purchase has been done
def create_purchase():
  nonce_from_the_client = request.form["payment_method_nonce"]

