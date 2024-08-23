from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from os import getenv
import os
import importlib

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app(challenge="default"):
  global mail, db, login_manager
  app = Flask(__name__)

  app.config['MAIL_SERVER'] = getenv('MAIL_SERVER', 'localhost')
  app.config['MAIL_PORT'] = getenv('MAIL_PORT', 1025)
  app.config['MAIL_USERNAME'] = getenv('MAIL_USERNAME', '')
  app.config['MAIL_PASSWORD'] = getenv('MAIL_PASSWORD', '')
  app.config['MAIL_USE_TLS'] = getenv('MAIL_USE_TLS', False)
  app.config['MAIL_USE_SSL'] = getenv('MAIL_USE_SSL', False)
  app.config['CHALLENGE'] = getenv("CHALLENGE", challenge)
  app.config['UPLOAD_DIR'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "profiles")
  if getenv('SECRET_KEY', '') == 'testing':
    app.config['MAIL_SUPPRESS_SEND'] = True
  mail.init_app(app)

  app.config.from_object('config')

  db.init_app(app)

  login_manager.init_app(app)

  from app.account.views import profile, auth
  app.register_blueprint(profile.profile_blueprint, url_prefix='/api/v1/user')
  app.register_blueprint(auth.auth_blueprint, url_prefix='/api/v1/auth')

  from app.main.views import main, root
  app.register_blueprint(main.main_blueprint, url_prefix='/api/v1/')
  app.register_blueprint(root.root_blueprint, url_prefix='/')

  from app.robots.views import robots
  app.register_blueprint(robots.robots_blueprint, url_prefix='/api/v1/')

  @app.errorhandler(404)
  def not_found(error):
      return jsonify(status="error",message="Page not found"), 404

  @app.errorhandler(500)
  def not_found(error):
      return jsonify(status="error",message="Internal Server Error"), 500

  challenge = importlib.import_module('app.challenge.'+app.config['CHALLENGE'])
  
  with app.app_context():
    challenge.load(app)
    db.create_all()
    db_seed()
    challenge.seed(app)
  
  return app

def db_seed():
  from faker import Faker
  from app.account.models import User
  from app.robots.models import Robot
  from names import get_full_name
  from app.utils import get_random_string
  fake = Faker()
  if len(User.query.filter_by(admin=True).all()) == 0:
    admin_user = User.insert_admin(fake.simple_profile()['username'],get_random_string())
    for i in range(10):
      name = get_full_name()
      description = name+" is a dummy curl bot."
      Robot(name=name,description=description,url=fake.url(),credentials="",owner_id=admin_user.id).save()
    for u in range(10):
      user = User.insert_user(fake.simple_profile()['username'],get_random_string())
      for i in range(10):
        name = get_full_name()
      description = name+" is a dummy curl bot."
      Robot(name=name,description=description,url=fake.url(),credentials="",owner_id=user.id).save()

