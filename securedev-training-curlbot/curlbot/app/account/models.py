from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean(),default=False)
    reset_token = db.Column(db.String(128))
    avatar = db.Column(db.String(128), default="avatar.png")

    robots = db.relationship('Robot', backref='owner', lazy='dynamic')  

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,'pbkdf2:sha256:1')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.admin == True

    @classmethod
    def insert_user(cls, username, password):
        user = User(
                username=username,
                admin=False,
                )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user
    @classmethod
    def insert_admin(cls, username, password):
        admin = User(
                username=username,
                admin=True,
                )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin)
        return admin

@login_manager.user_loader
def load_user(user_id):
    """ User loader function

    Registered within Flask-Login
    """
    try:
        user_id = int(user_id)
    except ValueError:
        print("Could not convert data to an integer.")
        return None
    except:
        print("Unkown error when loading the user")
        return None
    return User.query.get(user_id)
