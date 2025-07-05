from app import db
from flask_login import UserMixin
from models.role import user_role

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    #role = db.Column(db.String(20), nullable=False)  # 'admin', 'supplier', 'consumer'
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    roles = db.relationship('Role', secondary=user_role, backref='users')

    def get_id(self):
        return str(self.id)

class Consumer(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # same as User.id
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(20))
    password = db.Column(db.String(255), nullable=False)



