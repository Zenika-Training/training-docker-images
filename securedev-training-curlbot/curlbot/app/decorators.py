from functools import wraps
from flask_login import current_user
from flask import jsonify

def admin_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if not current_user.is_admin():
      return jsonify(status="error", message="Unauthorized."), 401
    return f(*args, **kwargs)
  return decorated
