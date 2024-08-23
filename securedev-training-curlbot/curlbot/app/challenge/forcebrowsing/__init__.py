from flask import make_response
from random import randrange
from app.robots.models import Robot
from os import getenv

robots_file = """User-Agent: *
Disallow: /api/v1/admin/robots
"""

def get_robots_txt_file():
  response = make_response(robots_file, 200)
  response.mimetype = "text/plain"
  return response

def load(app):
  from app.challenge.forcebrowsing.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)

  app.view_functions['root.get_robots_txt_file'] = get_robots_txt_file


def seed(app):
  with app.app_context():
    if Robot.query.filter_by(credentials=getenv('FLAG')).count() == 0:
        robots = Robot.query.all()
        robot = robots[randrange(len(robots))]
        robot.credentials = getenv('FLAG')
        robot.save()
