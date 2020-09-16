from avengers_pkg import login
from datetime import datetime
from avengers_pkg import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    heroname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Requests', backref="requester", lazy="dynamic")

    # Returned when the User model is called.
    def __repr__(self):
        return '{} | {}'.format(self.heroname, self.phone_number)

    # Logic to Set a Secure Password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Logic to Check a Secure Password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User Loader Function used by Flask-Login  
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Requests(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    post_date = db.Column(db.DateTime, index=True, default=datetime.utcnow) 
    body = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Returned when the Request model is called.
    def __repr__(self):
        return '<Request: {}>'.format(self.body)
