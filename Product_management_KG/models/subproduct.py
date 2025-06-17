from utils.neo4j_helpers import run_write_query

def create_subproduct(sub_id, name, version, description, parent_id):
    query = """
    MATCH (parent:Product {id: $parent_id})
    CREATE (sub:SubProduct {
        id: $sub_id,
        name: $name,
        version: $version,
        description: $description
    })
    CREATE (sub)-[:CHILD_OF]->(parent)
    RETURN sub
    """
    return run_write_query(query, {
        "sub_id": sub_id,
        "name": name,
        "version": version,
        "description": description,
        "parent_id": parent_id
    })
