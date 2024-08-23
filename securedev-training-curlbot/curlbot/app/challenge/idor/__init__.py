from flask_login import login_required
from app.robots.models import Robot
from flask import jsonify
from os import getenv
from random import randrange

@login_required
def get_robot(robot_id):
  robot = Robot.query.filter_by(id=robot_id).first()
  return jsonify(status="success", id=robot.id, name=robot.name, description=robot.description, url=robot.url, credentials=robot.credentials)

def load(app):
      # Overwrite route here.
  # Follow documentation at https://docs.ctfd.io/docs/plugins/#modifying-existing-routes
  app.view_functions['robots.get_robot'] = get_robot

def seed(app):
  if Robot.query.filter_by(credentials=getenv('FLAG')).count() == 0:
    robots = Robot.query.all()
    robot = robots[randrange(len(robots))]
    robot.credentials = getenv('FLAG')
    robot.save()
