from app import db

class Supplier(db.Model):
    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable=True)

    brand_id = db.Column(db.Integer, db.ForeignKey('plant_brand.id'), nullable=True)

    products = db.relationship('Product', backref='supplier', lazy=True)
    subproducts = db.relationship('SubProduct', backref='supplier', lazy=True)
