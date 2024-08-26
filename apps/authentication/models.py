# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from sqlalchemy.orm import relationship

from apps import db, login_manager

from apps.authentication.util import hash_pass
from werkzeug.security import generate_password_hash

from datetime import datetime
import pytz

def get_bogota_time():
    
    bogota_tz = pytz.timezone('America/Bogota')
    ahora_utc = datetime.now(pytz.utc)
    ahora = ahora_utc.astimezone(bogota_tz)
    return ahora
class UserBusiness(db.Model):
    __tablename__ = 'user_business'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)

    # Define relationships to Users and Businesses
    user = db.relationship("Users", back_populates="user_businesses")
    business = db.relationship("Businesses", back_populates="user_businesses")

    def __repr__(self):
        return f"<UserBusiness(id={self.id}, user_id={self.user_id}, business_id={self.business_id})>"
    
class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True)
    email         = db.Column(db.String(64), unique=True)
    password      = db.Column(db.LargeBinary)
    type_user = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(20), unique=True)
    email_token = db.Column(db.String(255), unique=True)
    active_account = db.Column(db.Boolean, default=False)
    token_created_at = db.Column(db.DateTime, default=get_bogota_time())

    # cash_register_sessions = relationship("CashRegisterSessions", back_populates="user")
    sessions = relationship("SessionLogs", back_populates="user")
    # Relationship to UserBusiness
    user_businesses = db.relationship("UserBusiness", back_populates="user")

    def __repr__(self):
        return str(self.username) 

    def encrypt_password(self, password):
        return hash_pass(password)
    
class SessionLogs(db.Model):
    __tablename__ = 'session_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    login_time = db.Column(db.DateTime, nullable=False)
    logout_time = db.Column(db.DateTime)

    # Establish relationship with Users
    user = relationship("Users", back_populates="sessions")

    def __repr__(self):
        return f"<SessionLogs(id={self.id}, user_id={self.user_id}, login_time={self.login_time}, logout_time={self.logout_time})>"
    
    
class BusinessTypes(db.Model):
    __tablename__ = 'business_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    # Define the relationship to Businesses
    businesses = db.relationship("Businesses", back_populates="business_type")

    def __repr__(self):
        return f"<BusinessTypes(id={self.id}, name='{self.name}')>"

class Businesses(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    payment_status = db.Column(db.Boolean, default=False)
    business_type_id = db.Column(db.Integer, db.ForeignKey('business_types.id'))
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(20), unique=True)
    is_authorized = db.Column(db.Boolean, default=False)

    # Define the relationship to BusinessTypes
    business_type = db.relationship("BusinessTypes", back_populates="businesses")
    # Relationship to UserBusiness
    user_businesses = db.relationship("UserBusiness", back_populates="business")

    def __repr__(self):
        return f"<Businesses(id={self.id}, name='{self.name}')>"

    
# class CashRegisterSessions(db.Model):
#     __tablename__ = 'cash_register_sessions'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
#     open_time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
#     close_time = db.Column(db.TIMESTAMP)
#     initial_cash = db.Column(db.Numeric, nullable=False)
#     # total_transactions = db.Column(db.Numeric, default=0)

#     # Relación con Usuarios
#     user = relationship("Users", back_populates="cash_register_sessions")

#     def __repr__(self):
#         return (f"<CashRegisterSessions(id={self.id}, user_id={self.user_id}, "
#                 f"open_time={self.open_time}, close_time={self.close_time}, "
#                 f"initial_cash={self.initial_cash})>")
      
@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


