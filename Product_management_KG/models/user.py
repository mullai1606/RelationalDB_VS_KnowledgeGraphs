import uuid
from extensions import neo4j_driver
from utils.neo4j_helpers import run_read_query, run_write_query


def create_user(user_id, name, email, password, role, contact=""):
    query = """
    CREATE (u:User {
        id: $id,
        name: $name,
        email: $email,
        password: $password,
        role: $role,
        contact: $contact
    })
    RETURN u
    """
    result = run_write_query(query, {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "contact": contact
    })
    return user_id

def get_user_by_email(email):
    query = "MATCH (u:User {email: $email}) RETURN u LIMIT 1"
    result = run_read_query(query, {"email": email})
    return result[0]['u'] if result else None

def get_user_by_id(user_id):
    query = "MATCH (u:User {id: $id}) RETURN u LIMIT 1"
    result = run_read_query(query, {"id": user_id})
    return result[0]['u'] if result else None