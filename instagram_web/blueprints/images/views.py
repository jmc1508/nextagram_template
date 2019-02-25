from app import app
from flask import Blueprint, render_template, request, redirect, url_for, flash
from instagram_web.util.upload import upload_file_to_s3, allowed_file

from werkzeug import secure_filename

from models.user import User


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

# @profile_photo_url
def update(id):
    
    # A
    if "profile_image" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["profile_image"]
    print(file)

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):

        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])

        user=User.get_by_id(id)
        user.profile_photo_path=file.filename
        breakpoint()
        user.save()
        flash('Profile photo updated')
        return redirect(url_for('users.edit',id=id))

    else:
        return render_template("home.html")
