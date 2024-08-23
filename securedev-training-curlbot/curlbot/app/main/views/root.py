from flask import Blueprint, render_template, current_app
import base64, json
from flask import make_response, send_from_directory, redirect, request

root_blueprint = Blueprint('root', __name__)
robots_file = """User-Agent: *
Disallow: /
"""

@root_blueprint.route('/profile/pic')
def get_profile_pic():
    pic = request.args.get('file')
    return send_from_directory(current_app.config['UPLOAD_DIR'], pic)

@root_blueprint.route('/public/<robot_base64>', methods=['GET'])
def get_robot_base64(robot_base64):
  return render_template('public_page.html',robot=json.loads(base64.urlsafe_b64decode(robot_base64)))

@root_blueprint.route('/app/<path:path>')
def send_app(path):
    return send_from_directory('front-app', path)

@root_blueprint.route('/app/')
def send_app_index():
    return send_from_directory('front-app', 'index.html')

@root_blueprint.route('/robots.txt', methods=['GET'])
def get_robots_txt_file():
  response = make_response(robots_file, 200)
  response.mimetype = "text/plain"
  return response

@root_blueprint.route('/')
def redirect_to_app():
    return redirect("/app/", code=302)