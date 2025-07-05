from utils.neo4j_helpers import run_write_query, run_read_query
import uuid

def create_consumer(user_id, name, email, contact):
    query = """
    MATCH (u:User {id: $user_id})
    SET u:Consumer
    SET u.contact = $contact
    RETURN u
    """
    return run_write_query(query, {
        "user_id": user_id,
        "name": name,
        "email": email,
        "contact": contact
    })

def get_consumer_by_id(consumer_id):
    query = "MATCH (c:Consumer {id: $id}) RETURN c LIMIT 1"
    result = run_read_query(query, {"id": consumer_id})
    return result[0]['c'] if result else None
