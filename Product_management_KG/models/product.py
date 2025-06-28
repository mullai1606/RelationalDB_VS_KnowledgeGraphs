from utils.neo4j_helpers import run_write_query, run_read_query

def create_category_if_not_exists(category_name):
    query = """
    MERGE (c:Category {name: $name})
    RETURN c
    """
    return run_write_query(query, {"name": category_name})

def create_brand_if_not_exists(brand_name):
    query = """
    MERGE (b:Brand {name: $name})
    RETURN b
    """
    return run_write_query(query, {"name": brand_name})

from utils.neo4j_helpers import run_write_query
import uuid

def create_product(name, description, cost, version, brand_id, category_id, supplier_id):
    product_id = str(uuid.uuid4())

    query = """
    MATCH (b:Brand {id: $brand_id})
    MATCH (c:Category {id: $category_id})
    MATCH (s:User {id: $supplier_id})
    CREATE (p:Product {
        id: $product_id,
        name: $name,
        description: $description,
        cost: $cost,
        version: $version
    })
    MERGE (p)-[:HAS_BRAND]->(b)
    MERGE (p)-[:HAS_CATEGORY]->(c)
    MERGE (s)-[:SUPPLIES]->(p)
    RETURN p
    """

    return run_write_query(query, {
        "product_id": product_id,
        "name": name,
        "description": description,
        "cost": cost,
        "version": version,
        "brand_id": brand_id,
        "category_id": category_id,
        "supplier_id": supplier_id
    })



def get_all_products():
    query = """
    MATCH (p:Product)
    OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Category)
    OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
    RETURN p, c.name AS category, b.name AS brand
    ORDER BY p.name
    """
    return run_read_query(query)

def get_product_by_id(product_id):
    query = """
    MATCH (p:Product {id: $product_id})
    OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Category)
    OPTIONAL MATCH (p)-[:HAS_BRAND]->(b:Brand)
    RETURN p, c.name AS category, b.name AS brand
    LIMIT 1
    """
    result = run_read_query(query, {"product_id": product_id})
    return result[0] if result else None
