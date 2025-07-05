from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import neo4j_driver
import uuid
from utils.neo4j_helpers import run_read_query, run_write_query
product_bp = Blueprint('product', __name__, url_prefix='/products')


import models.product as product_model
import models.plant_brand as brand_model
import models.category as category_model

product_bp = Blueprint('product', __name__)

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cost = float(request.form['cost'])
        version = request.form.get('version', '')
        brand_id = request.form['brand_id']
        category_id = request.form['category_id']

        # ✅ If user selected "Other", create/get category
        if category_id == "Other":
            custom_name = request.form.get('custom_category')
            if custom_name:
                category_result = category_model.get_or_create_category_by_name(custom_name)
                category_id = category_result[0]['c']['id']
            else:
                flash("Please enter a category name", "danger")
                return redirect(url_for('product.add_product'))

        product_model.create_product(name, description, cost, version, brand_id, category_id, current_user.id)
        flash("Product added successfully!", "success")
        return redirect(url_for('supplier.dashboard'))

    brands = brand_model.get_all_plant_brands()
    categories = category_model.get_all_categories()
    return render_template('product_templates/add_product.html', brands=brands, categories=categories)


# Product Detail View
@product_bp.route('/<product_id>')
def product_details(product_id):
    with neo4j_driver.session() as session:
        result = session.run(
            """
               MATCH (p:Product {id: $pid})
               OPTIONAL MATCH (p)-[:HAS_CATEGORY]->(c:Category)
               OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
               RETURN p, c, b

            """,
            pid=product_id
        ).single()

        subproducts_result = session.run(
            """
            MATCH (p:Product {id: $pid})<-[:IS_SUBPRODUCT_OF]-(s:SubProduct)
            RETURN s
            """,
            pid=product_id
        ).data()

    if not result:
        flash("Product not found.", "danger")
        return redirect(url_for('product.view_products'))

    product = result['p']
    category = result['c']
    brand = result['b']
    subproducts = [record['s'] for record in subproducts_result]

    return render_template(
        'product_templates/product_details.html',
        product=product,
        category=category,
        brand=brand,
        subproducts=subproducts
    )


# View All Products
@product_bp.route('/view')
def view_products():
    with neo4j_driver.session() as session:
        result = session.run("MATCH (p:Product) RETURN p").data()
        products = [record['p'] for record in result]
    return render_template('product_templates/view_products.html', products=products)


@product_bp.route('/add_subproduct', methods=['GET', 'POST'])
@login_required
def add_subproduct():
    if current_user.role != 'supplier':
        flash('Unauthorized', 'danger')
        return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        # Get all products supplied by current user
        products_result = session.run(
            """
            MATCH (s:User {id: $sid})-[:SUPPLIES]->(p:Product)
            RETURN p
            """,
            sid=current_user.id
        ).data()

    # ✅ Extract the product nodes
    products = [record['p'] for record in products_result]

    if request.method == 'POST':
        sub_id = str(uuid.uuid4())
        name = request.form['name']
        version = request.form.get('version', '')
        description = request.form['description']
        parent_product_id = request.form['parent_product_id']

        with neo4j_driver.session() as session:
            session.run(
                """
                MATCH (p:Product {id: $parent_id})
                CREATE (s:SubProduct {
                    id: $id,
                    name: $name,
                    version: $version,
                    description: $description
                })-[:IS_SUBPRODUCT_OF]->(p)
                """,
                id=sub_id,
                name=name,
                version=version,
                description=description,
                parent_id=parent_product_id
            )

        flash("Subproduct added successfully!", "success")
        return redirect(url_for('supplier.dashboard'))

    return render_template('product_templates/add_subproduct.html', products=products)


@product_bp.route('/purchase/<product_id>', methods=['POST'])
@login_required
def purchase_product(product_id):
    if current_user.role != 'consumer':
        flash('Only consumers can purchase products.', 'danger')
        return redirect(url_for('auth.login'))

    purchase_id = str(uuid.uuid4())

    with neo4j_driver.session() as session:
        session.run(
            """
            MATCH (u:User {id: $user_id}), (p:Product {id: $product_id})
            CREATE (u)-[:PURCHASED {
                id: $purchase_id,
                timestamp: timestamp()
            }]->(p)
            """,
            user_id=current_user.id,
            product_id=product_id,
            purchase_id=purchase_id
        )

    flash("Product purchased successfully!", "success")
    return redirect(url_for('product.rate_product', product_id=product_id))

@product_bp.route('/rate/<product_id>', methods=['GET', 'POST'])
@login_required
def rate_product(product_id):
    if current_user.role != 'consumer':
        flash('Only consumers can rate products.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form.get('comment', '')

        with neo4j_driver.session() as session:
            session.run(
                """
                MATCH (u:User {id: $user_id})-[r:PURCHASED]->(p:Product {id: $product_id})
                SET r.rating = $rating, r.comment = $comment
                """,
                user_id=current_user.id,
                product_id=product_id,
                rating=rating,
                comment=comment
            )

        flash("Rating submitted!", "success")
        return redirect(url_for('consumer.dashboard'))

    # ✅ Fetch the product name for display
    with neo4j_driver.session() as session:
        product_result = session.run(
            "MATCH (p:Product {id: $pid}) RETURN p.name AS name", pid=product_id
        ).single()

    product_name = product_result["name"] if product_result else "Product"

    return render_template(
        'consumer_templates/rate_product.html',
        product_id=product_id,
        product_name=product_name
    )

# @product_bp.route('/create_sample_categories')
# def create_sample_categories():
#     sample_categories = ['Productivity', 'Security', 'Development Tools', 'Media', 'Games']
#     with neo4j_driver.session() as session:
#         for cat in sample_categories:
#             category_id = str(uuid.uuid4())
#             session.run(
#                 "CREATE (c:Category {id: $id, name: $name})",
#                 id=category_id,
#                 name=cat
#             )
#     return "✅ Sample categories created!"

# @product_bp.route('/init_categories')
# def init_categories():
#     from models.category import create_category

#     default_categories = [
#         'Operating System', 'Music', 'Video_editing', 'Firmware',
#         'casual', 'Games', 'Development', 'plugin'
#     ]
#     for name in default_categories:
#         create_category(name)
    
#     return "✅ Default categories created in Neo4j."