from utils.neo4j_helpers import run_write_query, run_read_query
import uuid

def create_supplier(user_id, name, email, contact):
    query = """
    MATCH (u:User {id: $user_id})
    SET u:Supplier
    SET u.contact = $contact
    RETURN u
    """
    return run_write_query(query, {
        "user_id": user_id,
        "name": name,
        "email": email,
        "contact": contact
    })

def get_supplier_by_id(supplier_id):
    query = "MATCH (s:Supplier {id: $id}) RETURN s LIMIT 1"
    result = run_read_query(query, {"id": supplier_id})
    return result[0]['s'] if result else None
