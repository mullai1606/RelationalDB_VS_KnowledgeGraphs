# from app import db

# class SubProduct(db.Model):
#     __tablename__ = 'subproduct'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     version = db.Column(db.String(20), nullable=True)
#     description = db.Column(db.Text, nullable=True)
   
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=True)

from app import db

class SubProduct(db.Model):
    __tablename__ = 'subproduct'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=True)
    # The 'product' backref is automatically available from Product.subproducts
