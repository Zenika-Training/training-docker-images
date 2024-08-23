import pytest
from app import create_app ,db
import os, json
from app.account.models import User
from app.robots.models import Robot

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

def setup_function():
    app = create_app()
    with app.app_context():
      db.session.commit()
      db.drop_all()
      db.create_all()
    return app
  
def teardown_function():
    os.remove('app.db')

class TestRobotsClass:    
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


  
  def test_robots_list(self,client):
    assert client.get("/api/v1/robots").status_code == 401
    self.login_as_user(client)
    assert client.get("/api/v1/robots").status_code == 200
    assert client.get("/api/v1/robots").json == []
  
  def test_user_can_create_robot(self,client):
    assert client.post("/api/v1/robots").status_code == 401
    self.login_as_user(client)
    assert Robot.query.count() == 0
    assert self.post_json(client,"/api/v1/robots",{"name":"","description":"","url":"","credentials":""}).json['status'] == "success"
    assert Robot.query.count() == 1
    assert len(client.get("/api/v1/robots").json) == 1
    self.login_as_admin(client)
    assert len(client.get("/api/v1/robots").json) == 0
  
  def test_user_can_access_robot(self,client):
    self.login_as_user(client)
    robot_id = client.get("/api/v1/robots").json[0]['id']
    assert client.get("/api/v1/robot/"+str(robot_id)).status_code == 200
    assert client.get("/api/v1/robot/"+str(robot_id)).json["id"] == robot_id
  
  def test_user_can_update_robot(self,client):
    self.login_as_user(client)
    robot_id = client.get("/api/v1/robots").json[0]['id']
    assert self.put_json(client,"/api/v1/robot/"+str(robot_id),{"name":"NAME","description":"DESC","url":"URL","credentials":"CREDS"}).status_code == 200
    assert len(client.get("/api/v1/robots").json) == 1
    robot = Robot.query.filter_by(id=robot_id).first()
    assert robot.name == "NAME" and robot.description=="DESC" and robot.url=="URL" and robot.credentials == "CREDS"

  def test_user_can_search_robots(self, client):
    self.login_as_user(client)
    robot_name = client.get("/api/v1/robots").json[0]['name']
    assert len(self.post_json(client, "/api/v1/search", {"name":robot_name}).json['message']) == 1
    assert len(self.post_json(client, "/api/v1/search", {"name":"AAAAAAAAAA"}).json['message']) == 0

  def test_user_can_delete_robot(self,client):
    self.login_as_user(client)
    robot_id = client.get("/api/v1/robots").json[0]['id']
    assert client.delete("/api/v1/robot/"+str(robot_id)).status_code == 200
    assert len(client.get("/api/v1/robots").json) == 0
  
  def test_user_can_curl(self, client):
    self.login_as_user(client)
    assert "200" in self.post_json(client, "/api/v1/test_curl", {"url":"https://www.google.fr"}).json['message']

  
