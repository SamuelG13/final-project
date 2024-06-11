import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Getting the absolute path for the database
db_directory = os.path.abspath(os.path.dirname(__file__))

# Initializing SQLAlchemy and LoginManager
db = SQLAlchemy()
login_manager = LoginManager()

def create_application():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '3de8f7d294b3d6bee7d01504a59272df76d3a3e2913202e6dbba54eaf07eda95192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
   
    # App configurations for the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(db_directory, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initializing the database
    db.init_app(app)

    # Initializing the login_manager 
    login_manager.session_protection = "strong"
    login_manager.login_view = 'views.landing'   
    login_manager.init_app(app)

    # Importing and registering views for usual pages
    from .view import views
    app.register_blueprint(views, url_prefix='/')
    
    # Importing and registering views for authentication pages
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    return app
