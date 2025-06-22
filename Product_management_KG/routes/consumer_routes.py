from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import neo4j_driver
import uuid

consumer_bp = Blueprint('consumer', __name__, url_prefix='/consumer')

@consumer_bp.route('/dashboard')
@login_required
def dashboard():
    with neo4j_driver.session() as session:
        products = session.run("MATCH (p:Product) RETURN p").data()
        purchases = session.run(
            """
            MATCH (c:User {id: $cid})-[:PURCHASED]->(p:Product)
            RETURN p
            """, cid=current_user.id).data()
    return render_template('consumer_templates/dashboard.html', products=products, purchases=purchases)

@consumer_bp.route('/purchase/<product_id>', methods=['POST'])
@login_required
def purchase_product(product_id):
    with neo4j_driver.session() as session:
        session.run(
            """
            MATCH (u:User {id: $uid}), (p:Product {id: $pid})
            MERGE (u)-[:PURCHASED]->(p)
            """, uid=current_user.id, pid=product_id
        )
    flash('Product purchased successfully.', 'success')
    return redirect(url_for('consumer.dashboard'))

@consumer_bp.route('/rate/<product_id>', methods=['POST'])
@login_required
def rate_product(product_id):
    rating = request.form.get('rating')
    with neo4j_driver.session() as session:
        session.run(
            """
            MATCH (u:User {id: $uid})-[r:PURCHASED]->(p:Product {id: $pid})
            SET r.rating = $rating
            """, uid=current_user.id, pid=product_id, rating=int(rating)
        )
    flash('Product rated.', 'success')
    return redirect(url_for('consumer.dashboard'))
