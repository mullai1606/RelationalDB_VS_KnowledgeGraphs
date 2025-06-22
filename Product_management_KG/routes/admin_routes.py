from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from neo4j import GraphDatabase
from extensions import neo4j_driver


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized', 'danger')
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        users = session.run("MATCH (u:User) WHERE u.role <> 'admin' RETURN u").data()
        products = session.run("MATCH (p:Product) RETURN p").data()

    return render_template('admin_templates/dashboard.html', users=users, products=products)

@admin_bp.route('/delete_user/<user_id>')
@login_required
def delete_user(user_id):
    with neo4j_driver.session() as session:
        session.run("MATCH (u:User {id: $uid}) DETACH DELETE u", uid=user_id)
    flash('User deleted.', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_product/<product_id>')
@login_required
def delete_product(product_id):
    with neo4j_driver.session() as session:
        session.run("MATCH (p:Product {id: $pid}) DETACH DELETE p", pid=product_id)
    flash('Product deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
