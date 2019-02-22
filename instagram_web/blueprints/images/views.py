from app import app
from flask import Blueprint, render_template, request, redirect
from instagram_web.util.upload import upload_file_to_s3, allowed_file
# from werkzeug.security import secure_filename
from werkzeug import secure_filename


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
        print('We get to here now')
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("home.html")
