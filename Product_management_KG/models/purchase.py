from utils.neo4j_helpers import run_write_query, run_read_query

# Create a PURCHASED relationship from consumer to product
def create_purchase(consumer_id, product_id):
    query = """
    MATCH (c:Consumer {id: $consumer_id}), (p:Product {id: $product_id})
    MERGE (c)-[r:PURCHASED]->(p)
    RETURN r
    """
    return run_write_query(query, {
        "consumer_id": consumer_id,
        "product_id": product_id
    })

# Add or update rating on an existing PURCHASED relationship
def rate_product(consumer_id, product_id, rating):
    query = """
    MATCH (c:Consumer {id: $consumer_id})-[r:PURCHASED]->(p:Product {id: $product_id})
    SET r.rating = $rating
    RETURN r
    """
    return run_write_query(query, {
        "consumer_id": consumer_id,
        "product_id": product_id,
        "rating": rating
    })

# Get all products purchased by a consumer (with optional rating)
def get_purchased_products(consumer_id):
    query = """
    MATCH (c:Consumer {id: $consumer_id})-[r:PURCHASED]->(p:Product)
    OPTIONAL MATCH (p)-[:BELONGS_TO]->(cat:Category)
    OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
    RETURN p, r.rating AS rating, cat.name AS category, b.name AS brand
    """
    return run_read_query(query, {
        "consumer_id": consumer_id
    })

# Check if a user has already purchased a product
def has_purchased(consumer_id, product_id):
    query = """
    MATCH (c:Consumer {id: $consumer_id})-[r:PURCHASED]->(p:Product {id: $product_id})
    RETURN COUNT(r) AS count
    """
    result = run_read_query(query, {
        "consumer_id": consumer_id,
        "product_id": product_id
    })
    return result[0]["count"] > 0 if result else False
