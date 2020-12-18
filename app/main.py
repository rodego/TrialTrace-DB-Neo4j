
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_wtf import FlaskForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required, current_user
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, text
from uuid import uuid4
import asyncio
import re
import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

ENV = os.uname().sysname

if ENV == os.getenv("SYSTEM"):
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DATABASE_ADDRESS")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)


class UUserMixin(UserMixin):
    def get_id(self):
        try:
            return self.user_uid
        except AttributeError:
            raise NotImplementedError('No `user_uid` attribute - override `get_id`')

class Users(db.Model, UUserMixin):
    __tablename__ = 'users'
    user_uid = db.Column(UUID(as_uuid=True),
                          primary_key=True, default=uuid4, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, email, password, is_admin):
        self.email = email
        self.password = password
        self.is_admin = is_admin

class Whitelist(db.Model):
    __tablename__ = 'whitelist'
    domain_uid = db.Column(UUID(as_uuid=True),
                          primary_key=True, default=uuid4, nullable=False)
    domain = db.Column(db.String, nullable=False, unique=True)
    
    def __init__(self, domain):
        self.domain = domain


@login.user_loader
def load_user(user_id):
    return Users.query.get(user_id)