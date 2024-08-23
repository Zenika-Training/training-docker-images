from flask import request, jsonify
from flask_login import login_required
from app.account.models import User
from random import randrange
from os import getenv
from app import db
from sqlalchemy import text
from flask_login import current_user

@login_required
def get_robot(robot_id):
  query = 'SELECT id,name,description,url,credentials FROM robots WHERE owner_id="{}" AND id="{}"'.format(current_user.id,robot_id)
  result = db.session.execute(text(query)).all()
  print(query)
  print(result)
  if len(result) == 0: 
    return jsonify(status="error", message="Unauthorized"), 401
  else:
    row = result[0] 
    return jsonify(status="success", id=row[0], name=row[1], description=row[2], url=row[3], credentials=row[4])

      
def load(app):
  app.view_functions['robots.get_robot'] = get_robot

def seed(app): 
  admin = User.query.filter_by(id=1).first()
  admin.admin = False
  db.session.add(admin)
  db.session.commit()
  user = User.query.filter_by(id=5).first()
  user.admin = True
  user.avatar = getenv('FLAG')
  db.session.add(user)
  db.session.commit()
  