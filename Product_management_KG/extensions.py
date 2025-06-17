from neo4j import GraphDatabase

neo4j_driver = None

def init_neo4j(app):
    global neo4j_driver
    uri = app.config['NEO4J_URI']
    user = app.config['NEO4J_USERNAME']
    password = app.config['NEO4J_PASSWORD']
    neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
