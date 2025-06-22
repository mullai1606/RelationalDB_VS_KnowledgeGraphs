from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import neo4j_driver

import uuid

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    with neo4j_driver.session() as session:
        categories = session.run("MATCH (c:Category) RETURN c").data()
        brands = session.run("MATCH (b:Brand) RETURN b").data()

    if request.method == 'POST':
        pid = str(uuid.uuid4())
        name = request.form['name']
        cost = float(request.form['cost'])
        version = request.form['version']
        description = request.form['description']
        category_id = request.form.get('category_id')
        brand_id = request.form.get('brand_id')
        custom_category = request.form.get('custom_category')

        with neo4j_driver.session() as session:
            if custom_category:
                category_id = str(uuid.uuid4())
                session.run("CREATE (c:Category {id: $id, name: $name})", id=category_id, name=custom_category)

            session.run(
                """
                MATCH (s:User {id: $supplier_id}), (b:Brand {id: $brand_id}), (c:Category {id: $category_id})
                CREATE (p:Product {
                    id: $id, name: $name, cost: $cost,
                    version: $version, description: $description
                })
                CREATE (s)-[:SUPPLIES]->(p)
                CREATE (p)-[:HAS_BRAND]->(b)
                CREATE (p)-[:BELONGS_TO]->(c)
                """,
                id=pid, name=name, cost=cost, version=version,
                description=description, supplier_id=current_user.id,
                brand_id=brand_id, category_id=category_id
            )

        flash('Product added successfully!', 'success')
        return redirect(url_for('supplier.dashboard'))

    return render_template('product_templates/add_product.html', categories=categories, brands=brands)

@product_bp.route('/<product_id>')
def product_details(product_id):
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (p:Product {id: $pid})
            OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Category)
            OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
            RETURN p, c, b
            """, pid=product_id).single()

        subproducts = session.run(
            "MATCH (p:Product {id: $pid})<-[:IS_SUBPRODUCT_OF]-(s:SubProduct) RETURN s", pid=product_id).data()

    return render_template('product_templates/product_details.html', product=result, subproducts=subproducts)

@product_bp.route('/view')
def view_products():
    with neo4j_driver.session() as session:
        products = session.run("MATCH (p:Product) RETURN p").data()
    return render_template('product_templates/view_products.html', products=products)
