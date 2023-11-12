from . import db 
from flask_login import UserMixin

# A way to remember what Applications are active on the user's page
user_links = db.Table('user_links', 
                 db.Column('application_id', db.Integer, db.ForeignKey('application.id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    color = db.Column(db.String(150))
    status = db.Column(db.Boolean)
    link = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150), unique=False)
    links = db.relationship('Application', secondary=user_links, lazy='subquery', backref=db.backref('user', lazy=True))
