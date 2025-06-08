from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.product import Product
from models.plant_brand import PlantBrand
from models.supplier import Supplier

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')

@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    supplier_products = Product.query.filter_by(supplier_id=current_user.id).all()
    all_products = Product.query.all()

    return render_template('supplier_templates/dashboard.html',
                           products=supplier_products,
                           all_products=all_products)

@supplier_bp.route('/add_brand', methods=['GET', 'POST'])
@login_required
def add_brand():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        brand = PlantBrand(name=name, location=location)
        db.session.add(brand)
        db.session.commit()
        flash('Brand/Plant added successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))
    return render_template('supplier_templates/add_brand.html')
