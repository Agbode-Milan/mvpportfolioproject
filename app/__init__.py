from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set the secret key
    app.config['SECRET_KEY'] = 'e76cf24ec93fa449c1c6822ceba1113d'

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from .models import User  # Import your User model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
