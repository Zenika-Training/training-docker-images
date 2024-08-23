from flask import request, jsonify
import subprocess
from flask_login import login_required

@login_required
def post_test_curl():
  json_data = request.get_json(silent=True)
  url = json_data.get('url', None)
  creds = json_data.get('creds', None)
  if not url or url=="":
    return jsonify(status="error", message="Url is missing",)
  else:
    if not creds or creds=="":
      cmd = ['bash', '-c', "curl -s -I {} | head -n 1 | cut -d ' ' -f2-".format(url)]
    else:
      cmd = ['bash', '-c', "curl -s -I -u {} {} | head -n 1 | cut -d ' ' -f2-".format(creds,url)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE)
    return jsonify(status="success", message=result.stdout.decode('utf-8'))

def load(app):
      # Overwrite route here.
  # Follow documentation at https://docs.ctfd.io/docs/plugins/#modifying-existing-routes
  app.view_functions['robots.post_test_curl'] = post_test_curl

def seed(app):
  # Seed the challenge if needed.
  pass