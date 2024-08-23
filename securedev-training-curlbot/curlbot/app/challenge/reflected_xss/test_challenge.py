import pytest
import os, json
from app.account.models import User
from app import create_app ,db
from os import getenv

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

@pytest.fixture
def app():
    app = create_app('reflected_xss')
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def setup_function():
    app = create_app('reflected_xss')
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        from app.challenge.reflected_xss import seed
        seed(app)
    return app
  
def teardown_function():
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
  
  def test_challenge_is_exploitable(self, client):
    resp = str(client.get("/public/eyJpZCI6MSwibmFtZSI6IjxzY3JpcHQ%2BYWxlcnQoMSk8L3NjcmlwdD4ifQ%3D%3D").data)
    assert "<script>alert(1)</script>" in resp
    assert self.post_json(client,"/api/v1/auth/login",{"login": "xssbot", "password": "xssbottesting"}).json['status'] == "success"
    assert client.get("/api/v1/flag").status_code == 200
    assert client.get("/api/v1/flag").json['message'] == getenv('FLAG')
