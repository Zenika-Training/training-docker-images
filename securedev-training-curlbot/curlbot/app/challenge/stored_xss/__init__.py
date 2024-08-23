from os import getenv
from app.account.models import User
from flask import render_template
from app.main.models import Contact
from app.decorators import admin_required
from flask import request, jsonify, render_template, current_app
from app.main.models import Contact
from app.decorators import admin_required
from selenium import webdriver
import time

@admin_required
def get_contact(): 
  contact = Contact.query.first()
  if contact is None:
    return "No contact to show."
  contact.delete()
  return render_template('contact-xss.html',contact=contact)

def check_contact(BASE_URL):
  
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument("--enable-javascript")

  driver = webdriver.Chrome(options=chrome_options)
  driver.get(BASE_URL)
  script = """
  fetch('%sapi/v1/auth/login',{
    method: 'POST',
    body: JSON.stringify({login: "xssbot", password: "%s"}),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  }).then(function(response) {
    window.location = "/api/v1/contact"
  })
  """ % (BASE_URL, getenv('XSSBOT_PASSWORD','xssbottesting'))
  driver.execute_script(script)
  time.sleep(2)
  driver.quit()

def post_contact():
  json_data = request.get_json(silent=True)
  try:
    email= json_data['email']
    name= json_data['name']
    content = json_data['content']
    contact = Contact(email=email,name=name,content=content)
    contact.save()
  except:
    return jsonify(status="error", message="Missing email,name or content",)

  if not current_app.config['TESTING']:
    check_contact("http://127.0.0.1:5000/")

  return jsonify(status="success", message="The administrator has read your message.")

def load(app):
  from app.challenge.cracking.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)
  app.view_functions['main.get_contact'] = get_contact
  app.view_functions['main.post_contact'] = post_contact
  app.config['SESSION_COOKIE_HTTPONLY'] = False

def seed(app):
  password = getenv('XSSBOT_PASSWORD')
  if password is None:
    User.insert_admin("xssbot", 'xssbottesting')
  else:
    User.insert_admin("xssbot", password)
