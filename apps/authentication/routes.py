# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for,flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager,mail
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm,EmailForm,PassForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass

from flask_mail import Message
from flask import current_app as app
import os
import uuid

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()



    if login_form.validate_on_submit():
        # read form data
        username = login_form.username.data
        password = login_form.password.data
            # Locate user
        user = Users.query.filter_by(username=username).first()
        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)

            if user.type_user == 1:
                return redirect(url_for('admin_blueprint.business_panel'))
            elif user.type_user == 2:
                return redirect(url_for('order_blueprint.order'))

        
        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Usuario o contraseña incorrectos',
                               form=login_form)

    else:
        return render_template('accounts/login.html',
                        form=login_form)
    # if not current_user.is_authenticated:
    #     return render_template('accounts/login.html',
    #                            form=login_form)



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm()
    if create_account_form.validate_on_submit():

        username = create_account_form.username.data
        email = create_account_form.email.data
        phone = create_account_form.phone.data
        password = create_account_form.password.data

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Nombre de usuario ya registrado',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Correo electrónico ya registrado',
                                   success=False,
                                   form=create_account_form)
        
        user = Users.query.filter_by(phone=phone).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Teléfono ya registrado',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        verificacion_email = str(uuid.uuid4())
        user = Users(email=email,username=username,phone=phone,password=Users().encrypt_password(password))
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Revisa tu correo electronico para la activacion correcta de la cuenta',
                               success=True,
                               form=create_account_form)

    else:
        print(create_account_form.confirm.errors)
        msg=""
        if create_account_form.confirm.errors:
            msg="Las contraseñas deben coincidir"

        return render_template('accounts/register.html', form=create_account_form,msg=msg)
    

@blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = EmailForm()
    if form.validate_on_submit():
        existing_email = Users.query.filter_by(email=form.email.data).first()
        if existing_email is not None:
            #login_user(user)  # Log in as newly created user
            email_info = Message('Cambiar contraseña', sender = app.config['MAIL_USERNAME'], recipients = [form.email.data])
            activate_link = app.config['DOMAIN']+ url_for('authentication_blueprint.password', email=str(form.email.data))
            email_info.body = render_template('accounts/email/template-reset-password.html', link=activate_link)
            email_info.html = render_template('accounts/email/template-reset-password.html', link=activate_link)

            for i in range(1, 8):
                img_name = f'image-{i}.png'
                img_path = os.path.join(app.static_folder, 'assets/img/email', img_name)
                with app.open_resource(img_path) as fp:
                    cid = f'<imagen_{i}>'
                    headers = {'Content-ID': cid}
                    email_info.attach(img_name, 'image/png', fp.read(), headers=headers)

            mail.send(email_info)
            return render_template("accounts/validate-email.html")
        
        flash("El correo no se encuentra registardo", "error")
    print(form.errors)  # Print form errors to debug

    return render_template(
        "accounts/forgot-password.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )

@blueprint.route('/password/<string:email>', methods=['GET'])
def password(email):
    form = PassForm()
    user = Users.query.filter_by(email=email).first()
    return render_template("accounts/reset-password.html", form=form, user=str(user.email), title="Create an Account.", template="signup-page", body="Sign up for a user account.",)

@blueprint.route('/word/<string:email>', methods=['POST'])
def word(email):
    form = PassForm()
    user = Users.query.filter_by(email=email).first()
    print("este es el usuario: ",user)
    if form.validate_on_submit():
        password = form.password.data

        print(password)
        update=Users.query.filter_by(email=user.email).update({Users.password: Users().encrypt_password(password)})
        print(update)
        db.session.commit() 
        login_user(user)

        if user.type_user == 1:
            return redirect(url_for('admin_blueprint.business_panel'))
        elif user.type_user == 2:
            return redirect(url_for('order_blueprint.order'))
        
    return render_template("accounts/reset-password.html", title="Create an Account.", user=str(user.email), form=form, template="signup-page", body="Sign up for a user account.",)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
