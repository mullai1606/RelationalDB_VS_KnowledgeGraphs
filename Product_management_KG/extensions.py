

# neo4j_driver = None
# login_manager = LoginManager()

# def init_neo4j(app):
#     global neo4j_driver
#     from neo4j import GraphDatabase
#     uri = app.config['NEO4J_URI']
#     user = app.config['NEO4J_USERNAME']
#     password = app.config['NEO4J_PASSWORD']
#     neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))

#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'

#     # Import here to avoid circular import
#     from models import user

#     @login_manager.user_loader
#     def load_user(user_id):
#         return user.get_user_by_id(user_id)

#///
# from models.neo4j_user import Neo4jUser

# def init_neo4j(app):
#     global neo4j_driver
#     uri = app.config['NEO4J_URI']
#     user = app.config['NEO4J_USERNAME']
#     password = app.config['NEO4J_PASSWORD']
#     neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))

#     # ✅ Login manager setup
#     login_manager.init_app(app)
#     login_manager.login_view = 'auth.login'

#     @login_manager.user_loader
#     def load_user(user_id):
#         user_node = user_model.get_user_by_id(user_id)
#         if user_node:
#             return Neo4jUser(
#                 id=user_node['id'],
#                 name=user_node['name'],
#                 email=user_node['email'],
#                 role=user_node['role']
#             )
#         return None


# from flask_login import LoginManager

# login_manager = LoginManager()
#option 2
# neo4j_driver = None

# def init_neo4j(app):
#     global neo4j_driver
#     uri = app.config['NEO4J_URI']
#     user = app.config['NEO4J_USERNAME']
#     password = app.config['NEO4J_PASSWORD']
#     neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
#     print("✅ Neo4j driver initialized.")

# def get_db():
#     if not neo4j_driver:
#         raise Exception("Neo4j driver is not initialized")
#     return neo4j_driver

# print("Neo4j driver initialized:", neo4j_driver)

from neo4j import GraphDatabase

neo4j_driver = None

def init_neo4j(app):
    global neo4j_driver
    uri = app.config['NEO4J_URI']
    user = app.config['NEO4J_USERNAME']
    password = app.config['NEO4J_PASSWORD']
    neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
    print("✅ Neo4j driver initialized.")

def get_db():
    if not neo4j_driver:
        raise Exception("Neo4j driver not initialized")
    return neo4j_driver

