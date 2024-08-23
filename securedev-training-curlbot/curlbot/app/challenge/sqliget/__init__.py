from flask import request, jsonify
from flask_login import login_required
from app.robots.models import Robot
from random import randrange
from os import getenv
from app import db
from sqlalchemy import text
from flask_login import current_user

@login_required
def get_robot(robot_id):
  query = 'SELECT id,name,description,url,credentials FROM robots WHERE owner_id="{}" AND id="{}"'.format(current_user.id,robot_id)
  result = db.session.execute(text(query)).all()
  if len(result) == 0: 
    return jsonify(status="error", message="Unauthorized"), 401
  else:
    row = result[0] 
    return jsonify(status="success", id=row[0], name=row[1], description=row[2], url=row[3], credentials=row[4])

      
def load(app):
  app.view_functions['robots.get_robot'] = get_robot

def seed(app): 
  if Robot.query.filter_by(credentials=getenv('FLAG')).count() == 0:
    robots = Robot.query.all()
    robot = robots[randrange(len(robots))]
    robot.credentials = getenv('FLAG')
    robot.save()
  