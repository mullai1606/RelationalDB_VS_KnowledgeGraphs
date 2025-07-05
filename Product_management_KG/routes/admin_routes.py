from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import neo4j_driver

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        # Get non-admin users
        users = session.run(
            """
            MATCH (u:User) WHERE u.role <> 'admin'
            RETURN u
            """
        ).data()

        # Get products with brand and category
        product_records = session.run(
            """
            MATCH (p:Product)
            OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
            OPTIONAL MATCH (p)-[:HAS_CATEGORY]->(c:Category)
            RETURN p, b.name AS brand, c.name AS category
            """
        ).data()

        # Format the data for the template
        products = []
        for record in product_records:
            p = record['p']
            p['brand'] = record.get('brand', 'N/A')
            p['category'] = record.get('category', 'N/A')
            products.append({'p': p})

    return render_template('admin_templates/dashboard.html', users=users, products=products)


@admin_bp.route('/delete_user/<user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        session.run("MATCH (u:User {id: $uid}) DETACH DELETE u", uid=user_id)

    flash("User deleted successfully!", "success")
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/delete_product/<product_id>')
@login_required
def delete_product(product_id):
    if current_user.role != 'admin':
        flash("Unauthorized", "danger")
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        session.run("MATCH (p:Product {id: $pid}) DETACH DELETE p", pid=product_id)

    flash("Product deleted successfully!", "success")
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        users = session.run(
            """
            MATCH (u:User) WHERE u.role <> 'admin'
            RETURN u
            """
        ).data()

    return render_template('admin_templates/manage_users.html', users=users)

@admin_bp.route('/view_all_products')
@login_required
def view_all_products():
    if current_user.role != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        products = session.run("MATCH (p:Product) RETURN p").data()

    return render_template('admin_templates/view_all_products.html', products=products)
