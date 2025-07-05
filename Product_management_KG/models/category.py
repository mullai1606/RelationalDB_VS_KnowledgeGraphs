from utils.neo4j_helpers import run_write_query, run_read_query
import uuid

def create_category(name):
    category_id = str(uuid.uuid4())
    query = """
    CREATE (c:Category {
        id: $id,
        name: $name
    }) RETURN c
    """
    return run_write_query(query, {
        "id": category_id,
        "name": name
    })



def get_or_create_category_by_name(name):
    query = """
    MERGE (c:Category {name: $name})
    ON CREATE SET c.id = $id
    RETURN c
    """
    return run_write_query(query, {
        "name": name,
        "id": str(uuid.uuid4())
    })

def get_all_categories():
    query = "MATCH (c:Category) RETURN c ORDER BY c.name"
    result = run_read_query(query)

    # Extract just the id and name into a list of dicts
    return [{'id': r['c']['id'], 'name': r['c']['name']} for r in result]