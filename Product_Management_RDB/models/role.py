from app import db
from flask_login import UserMixin

#Additional requirement to validate the application 
# models/role.py
class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

from sqlalchemy import Table, Column, Integer, ForeignKey


user_role = Table('user_role', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)
