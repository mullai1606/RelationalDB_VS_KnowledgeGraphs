from utils.neo4j_helpers import run_write_query, run_read_query
import uuid
from datetime import datetime

def create_purchase(user_id, product_id):
    purchase_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    query = """
    MATCH (u:User {id: $user_id}), (p:Product {id: $product_id})
    CREATE (u)-[r:PURCHASED {
        id: $purchase_id,
        timestamp: $timestamp
    }]->(p)
    RETURN r
    """
    return run_write_query(query, {
        "user_id": user_id,
        "product_id": product_id,
        "purchase_id": purchase_id,
        "timestamp": timestamp
    })


def get_user_purchases(user_id):
    query = """
    MATCH (u:User {id: $user_id})-[r:PURCHASED]->(p:Product)
    OPTIONAL MATCH (p)<-[:SUB_OF]-(sub:SubProduct)
    RETURN p, r, collect(sub) AS subproducts
    ORDER BY r.timestamp DESC
    """
    return run_read_query(query, {"user_id": user_id})


def has_user_purchased(user_id, product_id):
    query = """
    MATCH (:User {id: $user_id})-[r:PURCHASED]->(:Product {id: $product_id})
    RETURN count(r) > 0 AS purchased
    """
    result = run_read_query(query, {
        "user_id": user_id,
        "product_id": product_id
    })
    return result[0]["purchased"] if result else False


def add_rating(user_id, product_id, rating):
    query = """
    MATCH (:User {id: $user_id})-[r:PURCHASED]->(:Product {id: $product_id})
    SET r.rating = $rating
    RETURN r
    """
    return run_write_query(query, {
        "user_id": user_id,
        "product_id": product_id,
        "rating": rating
    })


def get_rated_purchases(user_id):
    query = """
    MATCH (:User {id: $user_id})-[r:PURCHASED]->(p:Product)
    WHERE exists(r.rating)
    RETURN p.name AS product, r.rating AS rating
    ORDER BY r.rating DESC
    """
    return run_read_query(query, {"user_id": user_id})
