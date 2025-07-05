from utils.neo4j_helpers import run_write_query, run_read_query
import uuid

def create_subproduct(name, description, version, parent_product_id):
    subproduct_id = str(uuid.uuid4())

    query = """
    MATCH (parent:Product {id: $parent_id})
    CREATE (sub:SubProduct {
        id: $id,
        name: $name,
        description: $description,
        version: $version
    })
    MERGE (sub)-[:SUB_OF]->(parent)
    RETURN sub
    """
    return run_write_query(query, {
        "id": subproduct_id,
        "name": name,
        "description": description,
        "version": version,
        "parent_id": parent_product_id
    })

def get_subproducts_of_product(product_id):
    query = """
    MATCH (parent:Product {id: $product_id})<-[:SUB_OF]-(sub:SubProduct)
    RETURN sub
    ORDER BY sub.name
    """
    return run_read_query(query, {"product_id": product_id})
