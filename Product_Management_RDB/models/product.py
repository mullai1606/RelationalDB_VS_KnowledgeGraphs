from app import db
from enum import Enum
class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    #category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    version = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)

    
    plant_brand_id = db.Column(db.Integer, db.ForeignKey('plant_brand.id'))

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    subproducts = db.relationship('SubProduct', backref='product', cascade="all, delete-orphan")
