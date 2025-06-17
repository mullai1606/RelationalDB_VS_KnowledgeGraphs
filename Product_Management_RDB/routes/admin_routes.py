from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.product import Product
from models.user import User
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('auth.login'))
    
    users = User.query.all()
    products = Product.query.all()
    return render_template('admin_templates/dashboard.html', users=users, products=products)

@admin_bp.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('auth.login'))

    users = User.query.filter(User.role != 'admin').all()
    return render_template('admin_templates/manage_users.html', users=users)


@admin_bp.route('/view_products')
@login_required
def view_all_products():
    if current_user.role != 'admin':
        flash('Unauthorized access', 'danger')
        return redirect(url_for('auth.login'))

    products = Product.query.all()
    return render_template('admin_templates/view_all_products.html', products=products)
