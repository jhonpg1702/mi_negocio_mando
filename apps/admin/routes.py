# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.admin import blueprint
from flask import render_template, request,jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.authentication.models import Users 



@blueprint.route('/business_panel')
@login_required
def business_panel():

    return render_template("admin/business_list.html",segment="business_panel")


@blueprint.route("/business_list_data", methods=["GET", "POST"])
@login_required
def business_list_data():

    users = Users.query.filter(Users.type_user != 1).all()
        # Verifica si negocio es None, lo que significa que el usuario no se encuentra en la tabla Negocios
    if users is None:
        # Devuelve una lista vacía si el usuario no se encuentra
        return jsonify({'data': []})

    data_json = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'type_user': user.type_user,
            'phone': user.phone

        } for user in users
    ]


    return jsonify({'data': data_json})

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
