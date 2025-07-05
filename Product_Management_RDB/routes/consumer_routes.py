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

# @consumer_bp.route('/purchase/<int:product_id>', methods=['POST'])
# @login_required
# def purchase_product(product_id):
#     flash(f"Product {product_id} purchased successfully! (mock)", 'success')
#     return redirect(url_for('consumer.dashboard'))

# @consumer_bp.route('/rate/<int:product_id>', methods=['POST'])
# @login_required
# def rate_product(product_id):
#     rating = request.form['rating']
#     flash(f"Rated product {product_id} with {rating} stars. (mock)", 'info')
#     return redirect(url_for('consumer.dashboard'))

from models.purchase import Purchase
from flask import jsonify

# @consumer_bp.route('/purchase/<int:product_id>', methods=['POST'])
# @login_required
# def purchase_product(product_id):
#     product = Product.query.get_or_404(product_id)

#     # Save purchase
#     purchase = Purchase(consumer_id=current_user.id, product_id=product.id)
#     db.session.add(purchase)
#     db.session.commit()

#     flash('Product purchased successfully! Please provide a rating.', 'success')
#     return redirect(url_for('consumer.rate_product', product_id=product.id))

# @consumer_bp.route('/rate/<int:product_id>', methods=['GET', 'POST'])
# @login_required
# def rate_product(product_id):
#     purchase = Purchase.query.filter_by(consumer_id=current_user.id, product_id=product_id).first_or_404()

#     if request.method == 'POST':
#         rating = float(request.form['rating'])
#         purchase.rating = rating
#         db.session.commit()
#         flash('Thanks for rating!', 'success')
#         return redirect(url_for('consumer.dashboard'))

#     return render_template('consumer_templates/rate_product.html', product=purchase.product)


@consumer_bp.route('/purchase/<int:product_id>', methods=['POST'])
@login_required
def purchase_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Prevent duplicate purchase
    existing = Purchase.query.filter_by(product_id=product_id, consumer_id=current_user.id).first()
    if existing:
        flash('You already purchased this product.', 'info')
    else:
        purchase = Purchase(product_id=product.id, consumer_id=current_user.id)
        db.session.add(purchase)
        db.session.commit()
        flash('Product purchased successfully!', 'purchase_success')  # Triggers popup

    return redirect(url_for('product.product_details', product_id=product.id))

@consumer_bp.route('/submit_rating', methods=['POST'])
@login_required
def submit_rating():
    data = request.get_json()
    product_id = data.get('product_id')
    rating = data.get('rating')

    purchase = Purchase.query.filter_by(product_id=product_id, consumer_id=current_user.id).first()
    if purchase:
        purchase.rating = int(rating)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 400