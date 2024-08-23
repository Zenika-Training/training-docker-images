from flask import request, jsonify
from app.account.models import User

def register():
  json_data = request.get_json(silent=True)

  try:
    username = json_data['login']
    password = json_data['password']
    if 'role' in json_data:
      role = json_data['role']
    else:
      role = 'user'
  except:
    return jsonify(status="error", message="Wrong credentials")

  user = User.query.filter_by(username=username).first()    

  if user is None: 
    if role == "admin":
      user = User.insert_admin(username, password)
    else:
      user = User.insert_user(username, password)

  return jsonify(status="success", message="If the login is available, the account is created.")

def load(app):
  from app.challenge.clientsidebypass.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)

  app.view_functions['auth.register'] = register

def seed(app):
  pass
