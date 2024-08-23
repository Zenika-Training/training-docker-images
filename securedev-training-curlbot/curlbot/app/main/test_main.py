import pytest
from app import create_app ,db, mail
import os, tempfile, json
from app.main.models import Contact, Broken
from app.account.models import User

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

def setup_function():
    app = create_app()
    with app.app_context():
      db.session.commit()
      db.drop_all()
      db.create_all()
  
def teardown_function():
    os.remove('app.db')
  

class TestMainClass:    
  @classmethod
  def setup_class(self):
    setup_function()

  @classmethod
  def teardown_class(self):
    teardown_function()

  def test_user_can_contact(self, client):
    assert Contact.query.count() == 0
    assert client.post("/api/v1/contact", data=json.dumps({"email": "email"}), headers=headers).json['status'] == "error"
    assert Contact.query.count() == 0
    assert client.post("/api/v1/contact", data=json.dumps({"email": "EMAIL","name":"NAME","content":"CONTENT"}), headers=headers).json['status'] == "success"
    assert Contact.query.count() == 1

  def test_user_cant_access_contact(self, client):
    User.insert_user("user","toto")
    client.post("/api/v1/auth/login", data=json.dumps({"login": "user", "password": "toto"}), headers=headers)
    assert client.get("/api/v1/contact").status_code == 401
  
  def test_admin_can_access_contact(self, client):
    User.insert_admin("admin","toto")
    client.post("/api/v1/auth/login", data=json.dumps({"login": "admin", "password": "toto"}), headers=headers)
    assert client.get("/api/v1/contact").status_code == 200
  
  def test_admin_can_read_contact(self, client):
    client.post("/api/v1/auth/login", data=json.dumps({"login": "admin", "password": "toto"}), headers=headers)
    client.post("/api/v1/contact", data=json.dumps({"email": "EMAIL","name":"NAME","content":"CONTENT"}), headers=headers)
    contact_page = str(client.get("/api/v1/contact").data)
    assert "EMAIL" in contact_page and "NAME" in contact_page and "CONTENT" in contact_page
    contact_page = str(client.get("/api/v1/contact").data)
    assert "No contact to show." in contact_page

  """
    Broken Link Tests
  """

  def test_user_can_send_broken(self, client):
    assert Broken.query.count() == 0
    assert client.get("/api/v1/broken?link=").json['status'] == "error"
    assert Broken.query.count() == 0
    assert client.get("/api/v1/broken?link=test").json['status'] == "success"
    assert Broken.query.count() == 1
  
  def test_user_cant_access_broken(self, client):
    client.post("/api/v1/auth/login", data=json.dumps({"login": "user", "password": "toto"}), headers=headers)
    assert client.get("/api/v1/link").status_code == 401
  
  def test_admin_can_access_broken(self, client):
    client.post("/api/v1/auth/login", data=json.dumps({"login": "admin", "password": "toto"}), headers=headers)
    assert client.get("/api/v1/link").status_code == 200
    assert Broken.query.count() == 0
  
  def test_admin_can_read_broken(self, client):
    client.post("/api/v1/auth/login", data=json.dumps({"login": "admin", "password": "toto"}), headers=headers)
    Broken(link="test_link").save()
    broken_link_page = str(client.get("/api/v1/link").data)
    assert 'window.location.href="test_link"' in broken_link_page
    broken_link_page = str(client.get("/api/v1/link").data)
    assert "No link to show." in broken_link_page
  
  def test_public_robot_page(self, client):
    resp = str(client.get("/public/eyJpZCI6MSwibmFtZSI6IlRlc3QgTmFtZSJ9").data)
    assert "Test Name" in resp

  def test_robots_txt_accessible(self, client):
    assert client.get("/robots.txt").status_code == 200
