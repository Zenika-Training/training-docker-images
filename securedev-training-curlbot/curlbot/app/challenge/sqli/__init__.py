from flask import request, jsonify
from flask_login import login_required
from app.robots.models import Robot
from random import randrange
from os import getenv
from app import db
from sqlalchemy import text

@login_required
def post_search():
  try:
    json_data = request.get_json(silent=True)
    sql_name = json_data["name"]
  except :
    return jsonify(status="error", message="name parameter is missing",)
  
  try:
    query = 'SELECT id, name, description, url FROM robots WHERE name like "%{}%"'.format(sql_name)
    result = db.session.execute(text(query))      
    return jsonify(status="success", message=[{
      "id": row[0],
      "name": row[1],
      "description": row[2],
      "url": row[3],
    } for row in result])
    
  except Exception as e:
    return jsonify(status="error", message=str(e))
      
def load(app):
      # Overwrite route here.
  # Follow documentation at https://docs.ctfd.io/docs/plugins/#modifying-existing-routes
  app.view_functions['robots.post_search'] = post_search

def seed(app): 
  if Robot.query.filter_by(credentials=getenv('FLAG')).count() == 0:
    robots = Robot.query.all()
    robot = robots[randrange(len(robots))]
    robot.credentials = getenv('FLAG')
    robot.save()
  