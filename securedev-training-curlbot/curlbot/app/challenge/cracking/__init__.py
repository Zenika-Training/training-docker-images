from app.account.models import User
from app.utils import get_random_string

def load(app):
  from app.challenge.cracking.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)


def seed(app):
  User.query.filter_by(username="admin").delete()
  for i in range(5):
    if i == 3:
      password = "zenika"
    else:
      password = get_random_string()
    User.insert_admin("admin"+str(i), password)
