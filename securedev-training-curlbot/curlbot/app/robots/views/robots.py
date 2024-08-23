from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.robots.models import Robot
from names import get_full_name
import subprocess

robots_blueprint = Blueprint('robots', __name__)

@robots_blueprint.route('/robots', methods=['GET'])
@login_required
def get_robots():
  robots = Robot.query.filter_by(owner=current_user).all()
  return jsonify([{ "id": x.id, "name": x.name, "url": x.url } for x in robots])

@robots_blueprint.route('/robots', methods=['POST'])
@login_required
def post_robots():
  json_data = request.get_json(silent=True)
  try:
    name = json_data["name"]
    description = json_data["description"]
    url = json_data["url"]
    credentials = json_data["credentials"]
   
    if name == "":
      name = get_full_name()
    if description == "":
      description = name+" is a dummy curl bot."

    if Robot.query.filter_by(name=name).count():
      return jsonify(status="error", message="Name already taken.")

    Robot(owner_id=current_user.id,name=name,description=description,url=url,credentials=credentials).save()
    return jsonify(status="success", message=f"The robot has been created.")
  except:
    pass
  return jsonify(status="error", message="Error during bot creation.")

@robots_blueprint.route('/robot/<robot_id>', methods=['GET'])
@login_required
def get_robot(robot_id):
  robot = Robot.query.filter_by(id=robot_id, owner=current_user).first()
  if robot is None: 
    return jsonify(status="error", message="Unauthorized"), 401
  else:
    return jsonify(status="success", id=robot.id, name=robot.name, description=robot.description, url=robot.url, credentials=robot.credentials)

@robots_blueprint.route('/robot/<robot_id>', methods=['DELETE'])
@login_required
def delete_robot(robot_id):
  robot = Robot.query.filter_by(id=robot_id, owner=current_user).first()
  if robot is None: 
    return jsonify(status="error", message="Unauthorized"), 401
  else:
    robot.delete()
    return jsonify(status="success", message="The robot has been deleted.")

@robots_blueprint.route('/robot/<robot_id>', methods=['PUT'])
@login_required
def put_robot(robot_id):
  robot = Robot.query.filter_by(id=robot_id, owner=current_user).first()
  if robot is None: 
    return jsonify(status="error", message="Unauthorized"), 401
  else:
    json_data = request.get_json(silent=True)
    try:
      name = json_data["name"]
      description = json_data["description"]
      url = json_data["url"]
      credentials = json_data["credentials"]
      robot.name = name
      robot.description = description
      robot.url = url
      robot.credentials = credentials
      robot.save()
    except:
      return jsonify(status="error", message="Error during bot modification.")
    return jsonify(status="success", message="The robot has been modified.")

@robots_blueprint.route('/search', methods=['POST'])
@login_required
def post_search():
  try:
    json_data = request.get_json(silent=True)
    robots = Robot.query.filter(Robot.name.like(json_data["name"])).all()
    return jsonify(status="success", message=[{ "id": x.id, "name": x.name, "description":x.description, "url": x.url } for x in robots])
  except :
    return jsonify(status="error", message="Name is missing for search function")

@robots_blueprint.route('/test_curl', methods=['POST'])
@login_required
def post_test_curl():
    json_data = request.get_json(silent=True)
    url = json_data.get('url', None)
    creds = json_data.get('creds', None)
    if not url or url=="":
        return jsonify(status="error", message="Url is missing")
    else:
        if not creds or creds=="":
            cmd = ["curl","-s","-I",url]
        else:
            cmd = ["curl","-s","-I","-u",creds,url]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        return jsonify(status="success", message=' '.join(result.stdout.decode('utf-8').split("\r")[0].split(' ')[-2:]))
        
    return jsonify(status="error", message="Error during curl test")
