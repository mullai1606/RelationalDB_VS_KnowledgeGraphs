from utils.neo4j_helpers import run_write_query, run_read_query

def create_product(product_id, name, description, cost, version):
    query = """
    CREATE (p:Product {
        id: $product_id,
        name: $name,
        description: $description,
        cost: $cost,
        version: $version
    })
    RETURN p
    """
    return run_write_query(query, {
        "product_id": product_id,
        "name": name,
        "description": description,
        "cost": cost,
        "version": version
    })

def link_product_to_category(product_id, category_name):
    query = """
    MATCH (p:Product {id: $product_id})
    MERGE (c:Category {name: $category_name})
    MERGE (p)-[:BELONGS_TO]->(c)
    """
    run_write_query(query, {
        "product_id": product_id,
        "category_name": category_name
    })

def link_product_to_supplier(product_id, supplier_id):
    query = """
    MATCH (p:Product {id: $product_id}), (s:Supplier {id: $supplier_id})
    MERGE (s)-[:SUPPLIES]->(p)
    """
    run_write_query(query, {
        "product_id": product_id,
        "supplier_id": supplier_id
    })

def get_all_products():
    query = """
    MATCH (p:Product)
    OPTIONAL MATCH (p)-[:BELONGS_TO]->(c:Category)
    OPTIONAL MATCH (p)<-[:SUPPLIES]-(s:Supplier)
    RETURN p, c.name AS category, s.name AS supplier
    """
    return run_read_query(query)
