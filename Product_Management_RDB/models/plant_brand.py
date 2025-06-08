# from app import db

# class PlantBrand(db.Model):
#     __tablename__ = 'plant_brand'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     location = db.Column(db.String(200), nullable=True)
#     suppliers = db.relationship('Supplier', backref='plant_brand', lazy=True)

from app import db

class PlantBrand(db.Model):
    __tablename__ = 'plant_brand'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)

    suppliers = db.relationship('Supplier', backref='plant_brand', lazy=True)
    # 'products' backref is automatically available from Product.plant_brand
