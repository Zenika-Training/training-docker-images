from flask_login import current_user, login_required
from flask import jsonify, request
from app.utils import get_random_string
from app import db, mail
from flask_mail import Message
import base64
from app.account.models import User

def reset_passwd():
  try:
    json_data = request.get_json(silent=True)
    token = base64.urlsafe_b64decode(json_data.get('token', '').encode()).decode()
    user_id = token.split(':')[0]
    username = token.split(':')[1]
    user = User.query.filter_by(username=username,id=user_id).first()
    user.set_password(json_data.get('password', ''))
    db.session.add(user)
    db.session.commit()
    return jsonify(status="success", message="Password has been changed"), 200
  except:
    return jsonify(status="error", message="The reset process failed"), 401

def reset():
  
  json_data = request.get_json(silent=True)
  username = json_data.get('login', '')
  try:
    user = User.query.filter_by(username=username).first()
    if user.is_admin():
        return jsonify(status="error", message="Unable to reset an account with administration right"), 200 
    else:
      reset_link = "{}:{}".format(user.id, user.username)
      token = base64.urlsafe_b64encode(reset_link.encode()).decode()
      #base_url = "{}://{}".format(request.headers.get("X-Forwarded-Proto", "http"), request.host)
      #reset_url = base_url+"/#/reset?token="+
      #msg = Message('Reset Your Password', sender=("Curlbot", 'app@curlbot.vulnerable'), recipients = ['{}@curlbot.vulnerable'.format(user.username)])
      #msg.body = "Hey {},\nYou can reset your password by click on the following link : {}\nRegards,\nCurbot".format(username, reset_url)
      #msg.html = "<p><b>Hey {},</b></p><p>You can reset your password by click on the following <a href=\"{}\">link</a></p><p>Regards,</p><p>Curlbot</p>".format(username, reset_url)
      #mail.send(msg)
      return jsonify(status="success", message="Email server not available. You can use this token to reset your account: "+token), 200 
  except:
    return jsonify(status="error", message="User not found"), 200 

def load(app):
  # Overwrite route here.
  # Follow documentation at https://docs.ctfd.io/docs/plugins/#modifying-existing-routes
  from app.challenge.reset.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)


  app.view_functions['auth.reset_passwd'] = reset_passwd
  app.view_functions['auth.reset'] = reset

def seed(app):
  User.insert_admin(username="admin",password=get_random_string())
  pass
