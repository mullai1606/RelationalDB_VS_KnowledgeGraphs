from utils.neo4j_helpers import run_write_query

def create_consumer(user_id, name, email, contact):
    query = """
    MATCH (u:User {id: $user_id})
    CREATE (c:Consumer {
        id: $user_id,
        name: $name,
        email: $email,
        contact: $contact
    })
    CREATE (c)-[:IS_USER]->(u)
    RETURN c
    """
    return run_write_query(query, {
        "user_id": user_id,
        "name": name,
        "email": email,
        "contact": contact
    })
