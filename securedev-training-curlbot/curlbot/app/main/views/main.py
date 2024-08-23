from flask import Blueprint, request, jsonify, render_template
from app.main.models import Contact, Broken
from app.decorators import admin_required

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/contact', methods=['POST'])
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

  return jsonify(status="success", message="The admin will read your message as soon as possible.")

@main_blueprint.route('/contact', methods=['GET'])
@admin_required
def get_contact(): 
  contact = Contact.query.first()
  if contact is None:
    return "No contact to show."
  contact.delete()
  return render_template('contact.html',contact=contact)

@main_blueprint.route('/broken', methods=['GET'])
def post_broken():
    try:
        link= request.args.get('link')
        if link == "":
          raise Exception("Missing Link.")
        else:
          broken = Broken(link=link)
          broken.save()
    except:
        return jsonify(status="error", message="Missing link.")

    return jsonify(status="success", message="The admin will click on your link as soon as possible to check the bot issue.")

@main_blueprint.route('/link', methods=['GET'])
@admin_required
def get_broken(): 
        broken = Broken.query.first()
        if broken is None:
                return "No link to show."
        broken.delete()
        return render_template('public_page_link.html',link=broken.link)