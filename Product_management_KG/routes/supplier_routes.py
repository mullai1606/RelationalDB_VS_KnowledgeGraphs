from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import neo4j_driver
import uuid

supplier_bp = Blueprint('supplier', __name__, url_prefix='/supplier')

# Supplier Dashboard - Shows own products + all available products
@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    with neo4j_driver.session() as session:
        own_products_result = session.run(
            """
            MATCH (s:User {id: $sid})-[:SUPPLIES]->(p:Product)
            RETURN p
            """, sid=current_user.id
        ).data()
        own_products = [record['p'] for record in own_products_result]

        all_products_result = session.run(
            "MATCH (p:Product) RETURN p"
        ).data()
        all_products = [record['p'] for record in all_products_result]

    return render_template(
    'supplier_templates/dashboard.html',
    products=own_products,
    available_products=all_products  # this also works
    )

# Add Brand page
@supplier_bp.route('/add_brand', methods=['GET', 'POST'])
@login_required
def add_brand():
    if request.method == 'POST':
        brand_name = request.form['name']
        location = request.form.get('location', '')
        brand_id = str(uuid.uuid4())

        with neo4j_driver.session() as session:
            session.run(
                """
                CREATE (b:Brand {id: $id, name: $name, location: $location})
                """,
                id=brand_id, name=brand_name, location=location
            )

        flash('Brand added successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('supplier_templates/add_brand.html')
