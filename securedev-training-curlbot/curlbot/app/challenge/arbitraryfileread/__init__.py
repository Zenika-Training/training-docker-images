from flask_login import login_required
from flask import request, send_from_directory, current_app

import os

@login_required
def get_profile_pic():
    pic = request.args.get('file')
    path = os.path.join(current_app.config['UPLOAD_DIR'], pic)
    if os.path.realpath(path) == "/app/flag":
       return os.getenv("FLAG")
    else:
      return send_from_directory(os.path.dirname(path), os.path.basename(path))
    

def load(app):
  # Overwrite route here.
  # Follow documentation at https://docs.ctfd.io/docs/plugins/#modifying-existing-routes
  app.view_functions['root.get_profile_pic'] = get_profile_pic
  

def seed(app):
  pass
