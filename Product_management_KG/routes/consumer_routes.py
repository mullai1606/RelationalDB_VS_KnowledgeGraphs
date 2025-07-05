from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import neo4j_driver
from utils.neo4j_helpers import run_read_query
consumer_bp = Blueprint('consumer', __name__, url_prefix='/consumer')

@consumer_bp.route('/dashboard')
@login_required
def dashboard():
    # if current_user.role != 'consumer':
    #     flash("Unauthorized access", "danger")
    #     return redirect(url_for('auth.login'))

    with neo4j_driver.session() as session:
        # All products
        all_products = session.run("MATCH (p:Product) RETURN p").data()

        # Products the user purchased
        purchased = session.run(
            """
            MATCH (u:User {id: $uid})-[r:PURCHASED]->(p:Product)
            OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
            RETURN p, r.rating AS rating, r.comment AS comment, b
            """,
            uid=current_user.id
        ).data()

    return render_template(
        'consumer_templates/dashboard.html',
        all_products=all_products,
        purchased=purchased
    )


@consumer_bp.route('/product/<product_id>')
@login_required
def product_details(product_id):
    query = """
    MATCH (p:Product {id: $pid})
    OPTIONAL MATCH (p)-[:HAS_CATEGORY]->(c:Category)
    OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
    RETURN p, c, b
    """
    product = run_read_query(query, {"pid": product_id})
    
    sub_query = """
    MATCH (p:Product {id: $pid})<-[:SUB_OF]-(s:SubProduct)
    RETURN s
    """
    subproducts = run_read_query(sub_query, {"pid": product_id})

    return render_template('product_templates/product_details.html',
                           product=product[0] if product else None,
                           subproducts=subproducts)
