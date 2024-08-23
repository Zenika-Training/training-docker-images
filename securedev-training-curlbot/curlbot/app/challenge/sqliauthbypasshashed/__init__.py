from flask import request, jsonify
from sqlalchemy import text
from app.account.models import User
from flask_login import login_user
from app import db

def login():
  json_data = request.get_json(silent=True)

  try:
    username = json_data['login']
    password = json_data['password']
  except:
    return jsonify(status="error", message="Wrong credentials"), 401 
  
  try:
    result = db.session.query(User).from_statement(
          text('SELECT * FROM users WHERE username="{}"'.format(username))
      ).all()
    
    results = [row for row in result]
    if len(results) == 0:
      return jsonify(status="error", message="Wrong credentials"), 401
    elif len(results) > 1:
      return jsonify(status="error", message="Too much users"), 401
    else:
      user = results[0]
      try:
        if not user.verify_password(password):
          return jsonify(status="error", message="{} is not a good value for hash {}".format(password, user.password_hash)), 401
        else:
          login_user(user)
          return jsonify(status="success", id=user.id, is_admin=user.admin, avatar=user.avatar, username=user.username)
      except Exception as e:
        print(e)
        return jsonify(status="error", message="{} is not a good value for hash {}".format(password, user.password_hash)), 401
  except Exception as e:
    return jsonify(status="error", message=str(e)), 401


  


def load(app):
  from app.challenge.sqliauthbypass.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)
  app.view_functions['auth.login'] = login

def seed(app):
  admin = User.query.filter_by(id=1).first()
  admin.admin = False
  db.session.add(admin)
  db.session.commit()
  user = User.query.filter_by(id=6).first()
  user.admin = True
  db.session.add(user)
  db.session.commit()