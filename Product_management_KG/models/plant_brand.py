from utils.neo4j_helpers import run_write_query, run_read_query

def create_brand(brand_id, name):
    query = """
    CREATE (b:Brand {id: $brand_id, name: $name})
    RETURN b
    """
    return run_write_query(query, {
        "brand_id": brand_id,
        "name": name
    })

def link_product_to_brand(product_id, brand_id):
    query = """
    MATCH (p:Product {id: $product_id}), (b:Brand {id: $brand_id})
    MERGE (p)-[:HAS_BRAND]->(b)
    """
    run_write_query(query, {
        "product_id": product_id,
        "brand_id": brand_id
    })

def get_all_brands():
    query = "MATCH (b:Brand) RETURN b"
    return run_read_query(query)
