from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import bcrypt

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    return app
