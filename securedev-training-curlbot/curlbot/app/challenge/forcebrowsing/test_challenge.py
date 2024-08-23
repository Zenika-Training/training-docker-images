import pytest
from app import create_app ,db, db_seed
import os, tempfile, json
from app.account.models import User
from unittest import mock

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

@pytest.fixture
def app():
    app = create_app('forcebrowsing')
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def setup_function():
    app = create_app('forcebrowsing')
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        db_seed()
        from app.challenge.forcebrowsing import seed
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

  def test_challenge_is_exploitable(self,client, app):
    os.environ['FLAG'] = "ThisIsMyFlag"
    db.session.commit()
    db.drop_all()
    db.create_all()
    db_seed()
    from app.challenge.forcebrowsing import seed
    seed(app)
    assert "/api/v1/admin/robots" in str(client.get("/robots.txt").data)
    assert "ThisIsMyFlag" in str(client.get("/api/v1/admin/robots").data)
