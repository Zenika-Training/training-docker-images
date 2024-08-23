from app.account.models import User

def load(app):
      # Overwrite route here.
  # Follow documentation at https://docs.ctfd.io/docs/plugins/#modifying-existing-routes
  from app.challenge.weak_password.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)

def seed(app):
  # Seed the challenge if needed.
  User.query.filter_by(username="admin").delete()
  User.insert_admin("admin","matrix")