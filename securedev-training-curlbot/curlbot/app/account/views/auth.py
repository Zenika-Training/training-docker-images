from flask import Blueprint, request, jsonify, current_app
from app.account.models import User
from flask_login import login_user, logout_user
import base64, hashlib, hmac, json
from app import db, mail
from app.utils import get_random_string
from flask_mail import Message
import uuid


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/reset', methods=['POST']) 
def reset():
  json_data = request.get_json(silent=True)
  username = json_data.get('login', '')
  try:
    user = User.query.filter_by(username=username).first()
    if user.is_admin():
      return jsonify(status="error", message="Unable to reset an account with administration right"), 200 
    else:
      token = str(uuid.uuid4())
      user.reset_token = token
      db.session.add(user)
      db.session.commit()
      #reset_url = request.base_url.replace('/api/v1/auth/reset', '')+"/#/reset?token="+token
      #msg = Message('Reset Your Password', sender=("Curlbot", 'app@curlbot.vulnerable'), recipients = ['{}@curlbot.vulnerable'.format(user.username)])
      #msg.body = "Hey {},\nYou can reset your password by click on the following link : {}\nRegards,\nCurbot".format(username, reset_url)
      #msg.html = "<p><b>Hey {},</b></p><p>You can reset your password by click on the following <a href=\"{}\">link</a></p><p>Regards,</p><p>Curlbot</p>".format(username, reset_url)
      #mail.send(msg)
      return jsonify(status="success", message="Email server not available. You can use this token to reset your account: "+token), 200 
  except:
    return jsonify(status="error", message="User not found"), 200 

@auth_blueprint.route('/login', methods=['POST']) 
def login():
  json_data = request.get_json(silent=True)

  try:
    username = json_data['login']
    password = json_data['password']
  except:
    return jsonify(status="error", message="Wrong credentials"), 401 

  user = User.query.filter_by(username=username).first()

  if user == None or not user.verify_password(password):
    return jsonify(status="error", message="Wrong credentials"), 401
  else:
    login_user(user)
    return jsonify(status="success", id=user.id, is_admin=user.admin, avatar=user.avatar, username=user.username)

@auth_blueprint.route('/logout', methods=['GET']) 
def logout():
  logout_user()
  return jsonify(status="success", message="Logged out")


@auth_blueprint.route('/register', methods=['POST'])
def register():
  json_data = request.get_json(silent=True)

  try:
    username = json_data['login']
    password = json_data['password']
  except:
    return jsonify(status="error", message="Wrong credentials")

  user = User.query.filter_by(username=username).first()    

  if user is None: 
    user = User.insert_user(username, password)

  return jsonify(status="success", message="If the login is available, the account is created.")

@auth_blueprint.route('/reset-password', methods=['POST'])
def reset_passwd():
  json_data = request.get_json(silent=True)
  try:
    token = json_data.get('token', '')
    user = User.query.filter_by(reset_token=token).first()
    user.set_password(json_data.get('password', ''))
    user.reset_token = None
    db.session.add(user)
    db.session.commit()
    return jsonify(status="success", message="Password has been changed"), 200
  except:
    return jsonify(status="error", message="The reset process failed"), 401
