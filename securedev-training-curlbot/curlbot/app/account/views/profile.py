from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user 

import binascii, os

from app import db
from app.account.models import User

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify(status="success", id=current_user.id, avatar=current_user.avatar, login=current_user.username, is_admin=current_user.admin)

@profile_blueprint.route('/avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'file' not in request.files:
        return jsonify(status="error", message="No file")
    file = request.files['file']
    if file.filename == '':
        return jsonify(status="error", message="No file")
    ext = file.filename.rsplit('.', 1)[-1].lower()
    directory = current_app.config['UPLOAD_DIR']
    if file and ext in ["png", "jpg", "jpeg"]:
        new_name = binascii.b2a_hex(os.urandom(4)).decode() + ext
        file.save(os.path.join(directory, "{}.{}".format(new_name, ext)))   
        user = User.query.filter_by(username=current_user.username).first()
        user.avatar = "{}.{}".format(new_name, ext)
        db.session.add(user)
        db.session.commit()
        return jsonify(status="success", message="Avatar changed", avatar=user.avatar)
    else:
        return jsonify(status="error", message="File not allowed")