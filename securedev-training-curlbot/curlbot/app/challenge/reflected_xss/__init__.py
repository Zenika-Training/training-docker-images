from app.account.models import User
from os import getenv
import json, base64
from flask import render_template
from flask import current_app, request, jsonify, render_template
from selenium import webdriver
import time
from urllib.parse import quote_plus

def get_robot_base64(robot_base64):
  return render_template('public_page-xss.html',robot=json.loads(base64.urlsafe_b64decode(robot_base64)))

def check_broken(BASE_URL, link):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument("--enable-javascript")

  driver = webdriver.Chrome(options=chrome_options)
  script = """
  fetch('%sapi/v1/auth/login',{
    method: 'POST',
    body: JSON.stringify({login: "xssbot", password: "%s"}),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
  })
  """ % (BASE_URL, getenv('XSSBOT_PASSWORD','xssbottesting'))
  driver.execute_script(script)
  time.sleep(1)
  driver.get(BASE_URL+"public/"+link)
  time.sleep(2)
  driver.quit()

def post_broken():
    try:
        link= request.args.get('link')
        if link == "":
          raise Exception("Missing Link.")
        else:
          if not current_app.config['TESTING']:
            check_broken("http://127.0.0.1:5000/", quote_plus(link.replace("/public/",""), safe=""))
    except:
        return jsonify(status="error", message="Missing link.")

    return jsonify(status="success", message="The admin has click on your link.")

def load(app):
  from app.challenge.cracking.views import challenge_blueprint
  app.register_blueprint(challenge_blueprint)
  
  app.view_functions['root.get_robot_base64'] = get_robot_base64
  app.view_functions['main.post_broken'] = post_broken
  app.config['SESSION_COOKIE_HTTPONLY'] = False

def seed(app):
  password = getenv('XSSBOT_PASSWORD')
  if password is None:
    User.insert_admin("xssbot", 'xssbottesting')
  else:
    User.insert_admin("xssbot", getenv('XSSBOT_PASSWORD'))