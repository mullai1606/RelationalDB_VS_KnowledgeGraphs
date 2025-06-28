from utils.neo4j_helpers import run_write_query, run_read_query
import uuid

def create_plant_brand(name):
    brand_id = str(uuid.uuid4())
    query = """
    CREATE (b:Brand {
        id: $id,
        name: $name
    })
    RETURN b
    """
    return run_write_query(query, {
        "id": brand_id,
        "name": name
    })

def get_all_plant_brands():
    query = "MATCH (b:Brand) RETURN b ORDER BY b.name"
    result = run_read_query(query)

    # Extract id and name from each brand node
    return [{'id': r['b']['id'], 'name': r['b']['name']} for r in result]

def get_plant_brand_by_id(brand_id):
    query = "MATCH (b:Brand {id: $id}) RETURN b LIMIT 1"
    result = run_read_query(query, {"id": brand_id})
    return result[0]['b'] if result else None
