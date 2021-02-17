
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, current_user
import re
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
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


    
    db.init_app(app)
    migrate.init_app(app,db)
    from api.models.data import Data
    from api.models.users import Users
    


    login.init_app(app)


    

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @login.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

        
    return app
        


