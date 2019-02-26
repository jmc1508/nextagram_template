import braintree
from app import app

# Configure the environment
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=app.config['BRAINTREE_MERCHANT_ID'],
        public_key=app.config['BRAINTREE_PUBLIC_KEY'],
        private_key=app.config['BRAINTREE_PRIVATE_KEY']
    )
)


# Braintree - generate a client token
# client_token = gateway.client_token.generate({
#     "customer_id": a_customer_id
# })

# Braintree - generate a client token
def client_token():
  return gateway.client_token.generate()