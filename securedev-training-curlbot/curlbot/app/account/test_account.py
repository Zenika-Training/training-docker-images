import pytest
from .models import User
from app import create_app ,db, mail
import os, json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def setup_function():
    app = create_app()
    with app.app_context():
      db.session.commit()
      db.drop_all()
      db.create_all()
  
def teardown_function():
    os.remove('app.db')

class TestUserClass:    
  @classmethod
  def setup_class(self):
    setup_function()

  @classmethod
  def teardown_class(self):
    teardown_function()
  
  def post_json(self,client, url ,data):
    return client.post(url, data=json.dumps(data), headers=headers)

  def test_user_is_not_admin(self):
    user = User(username="test")
    assert user.is_admin() == False

  def test_admin_is_admin(self, app):
    user = User.insert_admin("test","test")
    assert user.is_admin() == True

  def test_bad_user_login(self,client):
    User.insert_admin("admin","toto")
    login_request = client.post("/api/v1/auth/login", data=json.dumps({"login": "a", "password": "a"}), headers=headers)
    assert login_request.status_code == 401
    assert login_request.json == {'message': 'Wrong credentials', 'status': 'error'}
    login_request = client.post("/api/v1/auth/login", data=json.dumps({"login": "admin", "password": "a"}), headers=headers)
    assert login_request.status_code == 401
    assert login_request.json == {'message': 'Wrong credentials', 'status': 'error'}
    assert client.get("/api/v1/user/profile").status_code == 401

  def test_bad_good_login_and_logout(self,client, app):
    User.insert_user("toto","toto")
    login_request = client.post("/api/v1/auth/login", data=json.dumps({"login": "toto", "password": "toto"}), headers=headers)
    assert login_request.status_code == 200
    assert login_request.json['status'] == "success"
    login = client.get("/api/v1/user/profile")
    assert login.status_code == 200
    assert login.json['login'] == "toto"
    assert login.json['is_admin'] == False
    assert client.get("/api/v1/auth/logout").status_code == 200
    assert client.get("/api/v1/user/profile").status_code == 401
  
  def test_user_can_register(self,client):
    assert client.post("/api/v1/auth/register", data=json.dumps({"login": "test_register_user", "password": "test_register_user"}), headers=headers).status_code == 200
    login_request = client.post("/api/v1/auth/login", data=json.dumps({"login": "test_register_user", "password": "test_register_user"}), headers=headers)
    assert login_request.status_code == 200
    assert login_request.json['status'] == "success"
    login = client.get("/api/v1/user/profile")
    assert login.status_code == 200
    assert login.json['login'] == "test_register_user"
    assert User.query.filter_by(username="test_register_user").first().is_admin() == False
  
  def test_user_can_reset(self, client):
    client.post("/api/v1/auth/register", data=json.dumps({"login": "test_reset_user", "password": "test_reset_user"}), headers=headers)
    res = client.post("/api/v1/auth/reset", data=json.dumps({"login": "test_reset_user"}), headers=headers).json
    reset_token = res['message'].split(': ')[1]
    reset_request = client.post("/api/v1/auth/reset-password", data=json.dumps({"token": reset_token, "password": "newpassword"}), headers=headers)
    assert reset_request.status_code == 200
    reset_request = client.post("/api/v1/auth/reset-password", data=json.dumps({"token": reset_token, "password": "newpassword"}), headers=headers)
    assert reset_request.status_code == 401
    assert self.post_json(client,"/api/v1/auth/login",{"login": "test_reset_user", "password": "newpassword"}).json['status'] == "success"
    
