from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def check_if_admin(id):
    return load_user(id).is_admin != 0

def my_query(id):
    user = db.session.query(User).get(int(id)) #.filter(User.id == id).first()
    if user:
        return user

def waisay_wali_query():
    result = db.session.execute("select 10").fetchall()
    return result[0]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #is_admin = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.username)   

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)