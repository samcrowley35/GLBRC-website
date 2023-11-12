from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Application, User
from .starter_data import links
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user, link_list=current_user.links)

@views.route('/editlinks')
@login_required
def edit_links():
    active_link_ids = []
    for link in current_user.links:
        active_link_ids.append(link.id)

    applications = Application.query.all()
    link_info = []
    for a in applications:
        trio = []
        trio.append(a.name)
        if a.id in active_link_ids:            
            trio.append(True)
        else:
            trio.append(False)
        trio.append(a.id)
        link_info.append(trio)
        
    return render_template('editlinks.html', user=current_user, link_info=link_info)

@views.route('/change-status', methods=['POST'])
def change_status():
    l = json.loads(request.data)
    l_id = l['id']
    
    active_link_ids = []
    for link in current_user.links:
        active_link_ids.append(link.id)

    link = Application.query.filter_by(id = l_id).first()

    if l_id in active_link_ids:
        # Need to remove the link from the User's link list
        current_user.links.remove(link)
    else:
        # Add the link to the list if it's not already there, if it is, do nothing
        if l_id not in active_link_ids:
            current_user.links.append(link)

    db.session.commit()
    
    return jsonify({})

