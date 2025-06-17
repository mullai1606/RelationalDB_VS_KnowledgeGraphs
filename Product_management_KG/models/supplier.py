from utils.neo4j_helpers import run_write_query

def create_supplier(user_id, name, email, contact):
    query = """
    MATCH (u:User {id: $user_id})
    CREATE (s:Supplier {
        id: $user_id,
        name: $name,
        email: $email,
        contact: $contact
    })
    CREATE (s)-[:IS_USER]->(u)
    RETURN s
    """
    return run_write_query(query, {
        "user_id": user_id,
        "name": name,
        "email": email,
        "contact": contact
    })
