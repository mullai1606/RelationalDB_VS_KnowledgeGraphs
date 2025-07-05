import uuid
from extensions import neo4j_driver
from utils.neo4j_helpers import run_read_query, run_write_query


# def create_user(user_id, name, email, password, role, contact=""):
#     query = """
#     CREATE (u:User {
#         id: $id,
#         name: $name,
#         email: $email,
#         password: $password,
#         role: $role,
#         contact: $contact
#     })
#     RETURN u
#     """
#     result = run_write_query(query, {
#         "id": user_id,
#         "name": name,
#         "email": email,
#         "password": password,
#         "role": role,
#         "contact": contact
#     })
#     return user_id

# def get_user_by_email(email):
#     query = "MATCH (u:User {email: $email}) RETURN u LIMIT 1"
#     result = run_read_query(query, {"email": email})
#     return result[0]['u'] if result else None

# def get_user_by_id(user_id):
#     query = "MATCH (u:User {id: $id}) RETURN u LIMIT 1"
#     result = run_read_query(query, {"id": user_id})
#     return result[0]['u'] if result else None

def create_user(user_id, name, email, password, role, contact=""):
    query = """
    CREATE (u:User {
        id: $id,
        name: $name,
        email: $email,
        password: $password,
        contact: $contact
    })
    WITH u
    MERGE (r:Role {name: $role})
    MERGE (u)-[:HAS_ROLE]->(r)
    RETURN u
    """
    return run_write_query(query, {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password,
        "contact": contact,
        "role": role
    })

def get_user_by_email(email):
    query = """
    MATCH (u:User {email: $email})
    OPTIONAL MATCH (u)-[:HAS_ROLE]->(r:Role)
    RETURN u, collect(r) AS roles
    """
    result = run_read_query(query, {"email": email})

    if result:
        record = result[0]
        user_node = record['u']
        roles = record['roles']  # This is a list of Role nodes

        # Build a full user object with roles list
        return {
            "id": user_node['id'],
            "name": user_node.get('name', ''),
            "email": user_node.get('email', ''),
            "password": user_node.get('password', ''),
            "roles": [{"name": r["name"]} for r in roles]
        }

    return None

