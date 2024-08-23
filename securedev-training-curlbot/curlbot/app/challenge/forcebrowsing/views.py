from flask import Blueprint, jsonify
challenge_blueprint = Blueprint('challenge', __name__)
from app.robots.models import Robot


@challenge_blueprint.route('/api/v1/admin/robots', methods=['GET'])
def get_robots():
    robots = Robot.query.all()
    return jsonify(status="success", message=[{ "id": x.id, "name": x.name, "description": x.description, "url": x.url, "credentials": x.credentials} for x in robots])


