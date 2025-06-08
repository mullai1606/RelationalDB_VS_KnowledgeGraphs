from app import db
from datetime import datetime

class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    consumer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)

    consumer = db.relationship('User', backref='purchases')
    product = db.relationship('Product', backref='purchases')
