from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.product import Product
from app import db

consumer_bp = Blueprint('consumer', __name__, url_prefix='/consumer')

@consumer_bp.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.all()
    return render_template('consumer_templates/dashboard.html', products=products)

@consumer_bp.route('/purchase/<int:product_id>', methods=['POST'])
@login_required
def purchase_product(product_id):
    flash(f"Product {product_id} purchased successfully! (mock)", 'success')
    return redirect(url_for('consumer.dashboard'))

@consumer_bp.route('/rate/<int:product_id>', methods=['POST'])
@login_required
def rate_product(product_id):
    rating = request.form['rating']
    flash(f"Rated product {product_id} with {rating} stars. (mock)", 'info')
    return redirect(url_for('consumer.dashboard'))
