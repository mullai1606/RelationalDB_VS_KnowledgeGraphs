from extensions import neo4j_driver, get_db

# # Run a read-only Cypher query
# def run_read_query(query, parameters=None):
#     with neo4j_driver.session() as session:
#         result = session.read_transaction(lambda tx: tx.run(query, parameters or {}).data())
#         return result

# # Run a write Cypher query (CREATE, MERGE, DELETE, etc.)
# def run_write_query(query, parameters=None):
#     with neo4j_driver.session() as session:
#         result = session.write_transaction(lambda tx: tx.run(query, parameters or {}).data())
#         return result

def run_read_query(query, parameters=None):
    driver = get_db()
    with driver.session() as session:
        return session.run(query, parameters or {}).data()

def run_write_query(query, parameters=None):
    driver = get_db()
    with driver.session() as session:
        return session.run(query, parameters or {})

# Check if a node with a given label and property exists
def node_exists(label, property_key, value):
    query = f"""
    MATCH (n:{label} {{{property_key}: $value}})
    RETURN COUNT(n) AS count
    """
    result = run_read_query(query, {"value": value})
    return result[0]["count"] > 0 if result else False

# Create a node with label and properties
def create_node(label, properties):
    props = ", ".join([f"{k}: ${k}" for k in properties])
    query = f"CREATE (n:{label} {{ {props} }}) RETURN n"
    return run_write_query(query, properties)

# Delete node by label and property
def delete_node(label, property_key, value):
    query = f"""
    MATCH (n:{label} {{{property_key}: $value}})
    DETACH DELETE n
    """
    run_write_query(query, {"value": value})
