import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or os.urandom(32)
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION = f'http://{S3_BUCKET}.s3.amazonaws.com/'

# Braintree keys

    BRAINTREE_PUBLIC_KEY = os.environ.get("BRAINTREE_PUBLIC_KEY")
    BRAINTREE_PRIVATE_KEY = os.environ.get("BRAINTREE_PRIVATE_KEY")
    BRAINTREE_MERCHANT_ID = os.environ.get("BRAINTREE_MERCHANT_ID")

# Sendgrid Email Key

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# Google Oauth
    GOOGLE_CLIENT_ID=os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET=os.environ.get("GOOGLE_CLIENT_SECRET")

# Config for different environment
class ProductionConfig(Config):
    DEBUG = False
    ASSETS_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    ASSETS_DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    ASSETS_DEBUG = True
