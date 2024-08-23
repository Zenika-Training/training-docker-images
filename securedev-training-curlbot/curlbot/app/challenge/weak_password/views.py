from flask import Blueprint, jsonify
from flask_login import login_required
from app.decorators import admin_required
from os import getenv

challenge_blueprint = Blueprint('challenge', __name__)

@challenge_blueprint.route('/api/v1/flag', methods=['GET'])
@login_required
@admin_required
def flag_page():
    return jsonify(status="success",message=getenv('FLAG'))