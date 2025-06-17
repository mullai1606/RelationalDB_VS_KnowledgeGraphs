from utils.neo4j_helpers import run_write_query, run_read_query

def create_category_if_not_exists(name):
    query = """
    MERGE (c:Category {name: $name})
    RETURN c
    """
    return run_write_query(query, {"name": name})

def get_all_categories():
    query = "MATCH (c:Category) RETURN c.name AS name"
    return run_read_query(query)
