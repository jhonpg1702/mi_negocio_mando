# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import Email, DataRequired,EqualTo,Length

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    confirm = PasswordField(
        "Confirmar Contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    phone = StringField("Telefono", validators=[DataRequired()])
    submit = SubmitField("Registrarse")
    
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField("Telefono", validators=[DataRequired()])

    toc = BooleanField('Terms of Service', validators=[DataRequired()])
    
class EmailForm(FlaskForm):
    """User Log-in Form."""
 
    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Ingrese un email valido")]
    )     
    submit = SubmitField("Recuperar contraseña")

class PassForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6, message="Ingrese una contraseña segura"),],)
    confirm = PasswordField("Confirm password", validators=[DataRequired(),EqualTo("password", message="Las contraseñas no coinciden"),],)
    submit = SubmitField("Cambiar")