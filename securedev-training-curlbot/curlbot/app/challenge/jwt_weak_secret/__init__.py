
from flask import request, jsonify
from app.account.models import User
import jwt
from app import login_manager
from flask import current_app

@login_manager.request_loader
def load_user_from_request(r):
    session = r.cookies.get('session')
    if current_app.config['CHALLENGE'] == "jwt_weak_secret":
        try:
            data = jwt.decode(session, "123456", algorithms="HS256")
            user = User.query.filter_by(id=data['user_id']).all()[0]
            if user:
                return user
        except Exception:
            return None
        return None
    elif current_app.config['CHALLENGE'] == "jwt_signature_exclusion":
        try:
            if jwt.get_unverified_header(session)['alg'].lower() == "none":
                data = jwt.decode(session, current_app.config['SECRET_KEY'], options={"verify_signature": False})
            else:
                data = jwt.decode(session, current_app.config['SECRET_KEY'], algorithms="HS256")
            user = User.query.filter_by(id=data['user_id']).all()[0]
            if user:
                return user
        except Exception:
            return None
        return None

def login():
    json_data = request.get_json(silent=True)

    try:
        username = json_data['login']
        password = json_data['password']
    except Exception:
        return jsonify(status="error", message="Wrong credentials"), 401

    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return jsonify(status="error", message="Wrong credentials"), 401
    else:
        resp = jsonify(status="success", id=user.id, is_admin=user.admin, avatar=user.avatar, username=user.username)
        resp.set_cookie('session', jwt.encode(
          {"user_id": user.id}, '123456', algorithm="HS256")
          )
        return resp


def logout():
    resp = jsonify(status="success", message="Logged out")
    resp.set_cookie('session', '', expires=0)
    return resp


def load(app):
    from app.challenge.jwt_weak_secret.views import challenge_blueprint
    app.register_blueprint(challenge_blueprint)

    app.view_functions['auth.login'] = login
    app.view_functions['auth.logout'] = logout

def seed(app):
    # Seed the challenge if needed.
    pass
