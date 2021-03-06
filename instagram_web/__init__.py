from app import app
from flask import render_template
from flask_assets import Environment, Bundle
from .util.assets import bundles

from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect, CSRFError

from models.user import User


assets = Environment(app)
assets.register(bundles)

# Sendgrid API configuration
import sendgrid
sg = sendgrid.SendGridAPIClient(app.config['SENDGRID_API_KEY'])

# Add CSRF
csrf = CSRFProtect(app)

# # Add login manager
login_manager = LoginManager(app=app)
login_manager.login_view = "home"
login_manager.login_message = "Error: You need to be logged in to view this page"

# # Flask-Login user loader
@login_manager.user_loader
def load_user(id):
    return User.get_or_none(User.id == id)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Initialise blueprints

from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")


