from utils.neo4j_helpers import run_write_query, run_read_query

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
    return result[0]['u'] if result else None
