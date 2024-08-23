from flask import request, jsonify
from sqlalchemy import text
from app.account.models import User
from app import db
from flask_login import login_user
import hashlib

def login():
    json_data = request.get_json(silent=True)

    try:
        username = json_data['login']
        password = json_data['password']
    except:
        return jsonify(status="error", message="Wrong credentials"), 401 
    try:
        result = db.session.query(User).from_statement(
                text('SELECT * FROM users WHERE username="{}" and password_hash="{}"'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest()))
            ).all()
    except Exception as e:
        return jsonify(status="error", message=str(e))
    
    results = [row for row in result]
    if len(results) == 0:
        return jsonify(status="error", message="Wrong credentials"), 401
    elif len(results) > 1:
        return jsonify(status="error", message="Too much users"), 401
    else:
        user = results[0]
        login_user(user)
        return jsonify(status="success", id=user.id, is_admin=user.admin, avatar=user.avatar, username=user.username)

def set_password(self, password):
   self.password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

def verify_password(self, password):
    return self.password_hash == hashlib.md5(password.encode('utf-8')).hexdigest()

def load(app):
  from app.challenge.sqliauthbypass.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)

  app.view_functions['auth.login'] = login

  User.set_password = set_password
  User.verify_password = verify_password

def seed(app):
  admin = User.query.filter_by(id=1).first()
  admin.admin = False
  db.session.add(admin)
  db.session.commit()
  user = User.query.filter_by(id=4).first()
  user.admin = True
  db.session.add(user)
  db.session.commit()