from utils.neo4j_helpers import run_write_query, run_read_query
from models.neo4j_user import Neo4jUser

def create_user(user_id, name, email, password, role, contact):
    query = """
    CREATE (u:User {
        id: $user_id,
        name: $name,
        email: $email,
        password: $password,
        role: $role,
        contact: $contact
    })
    RETURN u
    """
    return run_write_query(query, {
        "user_id": user_id,
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "contact": contact
    })


def get_user_by_email(email):
    query = "MATCH (u:User {email: $email}) RETURN u LIMIT 1"
    result = run_read_query(query, {"email": email})
    if result:
        u = result[0]['u']
        return Neo4jUser(
            id=u['id'],
            name=u['name'],
            email=u['email'],
            password=u['password'],
            role=u['role'],
            contact=u.get('contact', '')
        )
    return None


def get_user_by_id(user_id):
    query = "MATCH (u:User {id: $id}) RETURN u LIMIT 1"
    result = run_read_query(query, {"id": user_id})
    if result:
        u = result[0]['u']
        return Neo4jUser(
            id=u['id'],
            name=u['name'],
            email=u['email'],
            password=u['password'],
            role=u['role'],
            contact=u.get('contact', '')
        )
    return None
