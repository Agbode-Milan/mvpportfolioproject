from flask_bcrypt import Bcrypt
import bcrypt
from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # selects mechaanic or driver
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    feedbacks = db.relationship('Feedback', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Feedback('{self.name}', '{self.email}', '{self.rating}', '{self.date_submitted}')"

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    expertise = db.Column(db.String(120), nullable=False)
    service_rates = db.Column(db.Float, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    feedbacks = db.relationship('Feedback', backref='mechanic', lazy=True)

    def __repr__(self):
        return f"Mechanic('{self.user_id}', '{self.expertise}')"

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_details = db.Column(db.String(200), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    feedbacks = db.relationship('Feedback', backref='driver', lazy=True)

    def __repr__(self):
        return f"Driver('{self.user_id}', '{self.vehicle_details}')"
