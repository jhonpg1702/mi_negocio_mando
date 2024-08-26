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

from apps import db, login_manager,mail,socketio
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm,EmailForm,PassForm,RegistrationForm
from apps.authentication.models import *
from apps.authentication.util import verify_pass
from flask import Flask, render_template, request, jsonify,session
from itsdangerous import URLSafeTimedSerializer
from flask_socketio import SocketIO, emit

from flask_mail import Message
from flask import current_app as app
import os
import time
@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()



    if request.method == 'POST':
        # read form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
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
        return render_template('authentication/sign-in.html',
                               msg='Usuario o contraseña incorrectos',
                               form=login_form)

    else:
        return render_template('authentication/sign-in.html',
                        form=login_form)
    # if not current_user.is_authenticated:
    #     return render_template('accounts/login.html',
    #                            form=login_form)
    
# @blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm()



#     if login_form.validate_on_submit():
#         # read form data
#         username = login_form.username.data
#         password = login_form.password.data
#             # Locate user
#         user = Users.query.filter_by(username=username).first()
#         # Check the password
#         if user and verify_pass(password, user.password):

#             login_user(user)

#             if user.type_user == 1:
#                 return redirect(url_for('admin_blueprint.business_panel'))
#             elif user.type_user == 2:
#                 return redirect(url_for('order_blueprint.order'))

        
#         # Something (user or pass) is not ok
#         return render_template('accounts/login.html',
#                                msg='Usuario o contraseña incorrectos',
#                                form=login_form)

#     else:
#         return render_template('accounts/login.html',
#                         form=login_form)
#     # if not current_user.is_authenticated:
#     #     return render_template('accounts/login.html',
#     #                            form=login_form)



@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    print(app.config['DOMAIN'])
    if request.method == 'POST':
        # Obtener datos del request
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        toc = request.form.get('toc')

        # Verificar si el usuario ya existe
        if Users.query.filter_by(username=username).first():
            return jsonify(success=False, message='Nombre de usuario ya registrado')

        # Verificar si el email ya existe
        if Users.query.filter_by(email=email).first():
            return jsonify(success=False, message='Correo electrónico ya registrado')

        # Verificar si el teléfono ya existe
        if Users.query.filter_by(phone=phone).first():
            return jsonify(success=False, message='Teléfono ya registrado')

        # Generar el token seguro
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email_token = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

        # Crear el enlace de activación
        activate_link = url_for('authentication_blueprint.activate', token=email_token, _external=True)

        # Configurar el correo electrónico
        email_info = Message('Confirma tu registro en Imperionex.com', sender=app.config['MAIL_USERNAME'], recipients=[email])
        email_info.body = render_template('authentication/email/template-verify-email.html', link=activate_link)
        email_info.html = render_template('authentication/email/template-verify-email.html', link=activate_link)

        # Adjuntar imágenes al correo electrónico
        for i in range(1, 6):
            img_name = f'image-{i}.png'
            img_path = os.path.join(app.static_folder, 'metronic/media/email/verify_email', img_name)
            with app.open_resource(img_path) as fp:
                cid = f'<imagen_{i}>'
                headers = {'Content-ID': cid}
                email_info.attach(img_name, 'image/png', fp.read(), headers=headers)

        # Enviar el correo
        mail.send(email_info)

        # Crear y guardar el usuario
        user = Users(email=email, phone=phone, password=Users().encrypt_password(password),
                     email_token=email_token, username=username, type_user=1)
        db.session.add(user)
        db.session.commit()

        # Guardar el correo en la sesión para mostrarlo en la página de verificación
        session['registered_email'] = email

        return jsonify(success=True, message="Registro exitoso! Revisa tu correo para activar tu cuenta.")

    return render_template('authentication/sign-up.html')

@blueprint.route('/login/activate/<token>', methods=['GET'])
def activate(token):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=86400)  # Expira en 24 hora
    except:
        return jsonify(success=False, message='El enlace de activación es inválido o ha expirado.')

    # Buscar al usuario por el email
    user = Users.query.filter_by(email=email).first()

    if user and user.email_token == token:
        user.active_account = 1
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('authentication_blueprint.multi_steps_register'))
    else:
        return jsonify(success=False, message='El enlace de activación es inválido.')


@blueprint.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    email = session.get('registered_email', None)

    if request.method == 'POST':
        if email:
            # Reenviar el correo de activación
            serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
            email_token = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
            
            user = Users.query.filter_by(email=email).first()
            user.email_token = email_token
            db.session.commit()
            
            activate_link = url_for('authentication_blueprint.activate', token=email_token, _external=True)

            email_info = Message('Reenvío de activación de cuenta en Imperionex.com', sender=app.config['MAIL_USERNAME'], recipients=[email])
            email_info.body = render_template('authentication/email/template-verify-email.html', link=activate_link)
            email_info.html = render_template('authentication/email/template-verify-email.html', link=activate_link)
            # Adjuntar imágenes al correo electrónico
            for i in range(1, 6):
                img_name = f'image-{i}.png'
                img_path = os.path.join(app.static_folder, 'metronic/media/email/verify_email', img_name)
                with app.open_resource(img_path) as fp:
                    cid = f'<imagen_{i}>'
                    headers = {'Content-ID': cid}
                    email_info.attach(img_name, 'image/png', fp.read(), headers=headers)
                
            mail.send(email_info)
            return jsonify(success=True, message='Correo de activación reenviado. Revisa tu bandeja de entrada.')

        else:
            return jsonify(success=False, message='No se encontró un correo registrado. Intenta registrarte nuevamente.')

    return render_template('authentication/general/verify-email.html', email=email)

@socketio.on('start_timer')
def handle_start_timer(data):
    total_time = data['time']
    for remaining_time in range(total_time, 0, -1):
        time.sleep(1)  # Esperar 1 segundo
        emit('update_timer', {'time': remaining_time}, broadcast=True)
    # Enviar mensaje cuando el temporizador ha terminado
    emit('timer_done', {}, broadcast=True)
@blueprint.route('/multi_steps_register', methods=['GET', 'POST'])
def multi_steps_register():
    queryTypes =BusinessTypes.query.all()
    if request.method == 'POST':
        business_name = request.form.get('business_name')
        business_type = request.form.get('business_type')
                # Verificar si el usuario ya ha enviado una solicitud
        existing_business = UserBusiness.query.filter_by(user_id=current_user.id).first()
        if existing_business:
            return jsonify(success=False, message='Ya has enviado una solicitud.')
        
        business = Businesses(name=business_name,business_type_id=business_type)
        db.session.add(business)
        
        userBusiness = UserBusiness(user_id=current_user.id,business_id=business.id)
        db.session.add(userBusiness)
        
        db.session.commit()

        return jsonify(success=True)

    return render_template('authentication/multi-steps-register.html',queryTypes=queryTypes,email=current_user.email)


        
# @blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     create_account_form = CreateAccountForm()
#     if create_account_form.validate_on_submit():

#         username = create_account_form.username.data
#         email = create_account_form.email.data
#         phone = create_account_form.phone.data
#         password = create_account_form.password.data

#         # Check usename exists
#         user = Users.query.filter_by(username=username).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Nombre de usuario ya registrado',
#                                    success=False,
#                                    form=create_account_form)

#         # Check email exists
#         user = Users.query.filter_by(email=email).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Correo electrónico ya registrado',
#                                    success=False,
#                                    form=create_account_form)
        
#         user = Users.query.filter_by(phone=phone).first()
#         if user:
#             return render_template('accounts/register.html',
#                                    msg='Teléfono ya registrado',
#                                    success=False,
#                                    form=create_account_form)

#         # else we can create the user
#         verificacion_email = str(uuid.uuid4())
#         user = Users(email=email,username=username,phone=phone,password=Users().encrypt_password(password))
#         db.session.add(user)
#         db.session.commit()

#         # Delete user from session
#         logout_user()
        
#         return render_template('accounts/register.html',
#                                msg='Revisa tu correo electronico para la activacion correcta de la cuenta',
#                                success=True,
#                                form=create_account_form)

#     else:
#         print(create_account_form.confirm.errors)
#         msg=""
#         if create_account_form.confirm.errors:
#             msg="Las contraseñas deben coincidir"

#         return render_template('accounts/register.html', form=create_account_form,msg=msg)
    

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
            return render_template("authentication/new-password.html")
        
        flash("El correo no se encuentra registardo", "error")
    print(form.errors)  # Print form errors to debug

    return render_template(
        "authentication/reset-password.html",
        title="Create an Account.",
        form=form,
        template="signup-page",
        body="Sign up for a user account.",
    )
# @blueprint.route("/forgot_password", methods=["GET", "POST"])
# def forgot_password():
#     form = EmailForm()
#     if form.validate_on_submit():
#         existing_email = Users.query.filter_by(email=form.email.data).first()
#         if existing_email is not None:
#             #login_user(user)  # Log in as newly created user
#             email_info = Message('Cambiar contraseña', sender = app.config['MAIL_USERNAME'], recipients = [form.email.data])
#             activate_link = app.config['DOMAIN']+ url_for('authentication_blueprint.password', email=str(form.email.data))
#             email_info.body = render_template('accounts/email/template-reset-password.html', link=activate_link)
#             email_info.html = render_template('accounts/email/template-reset-password.html', link=activate_link)

#             for i in range(1, 8):
#                 img_name = f'image-{i}.png'
#                 img_path = os.path.join(app.static_folder, 'assets/img/email', img_name)
#                 with app.open_resource(img_path) as fp:
#                     cid = f'<imagen_{i}>'
#                     headers = {'Content-ID': cid}
#                     email_info.attach(img_name, 'image/png', fp.read(), headers=headers)

#             mail.send(email_info)
#             return render_template("accounts/validate-email.html")
        
#         flash("El correo no se encuentra registardo", "error")
#     print(form.errors)  # Print form errors to debug

#     return render_template(
#         "accounts/forgot-password.html",
#         title="Create an Account.",
#         form=form,
#         template="signup-page",
#         body="Sign up for a user account.",
#     )

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
