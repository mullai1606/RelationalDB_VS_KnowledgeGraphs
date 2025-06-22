from neo4j import GraphDatabase

# === Update these with your actual Neo4j credentials ===
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "<your_password>"  # replace with your Neo4j password

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def run_query(tx, query, params=None):
    tx.run(query, params or {})

def init_data():
    with driver.session() as session:
        session.write_transaction(run_query, """
        // Clean existing data
        MATCH (n) DETACH DELETE n
        """)

        session.write_transaction(run_query, """
        // Create Admin User
        CREATE (:User {
            id: '1', name: 'Admin', email: 'admin@example.com',
            password: '$pbkdf2-sha256$29000$KtF6W3BhWh9KQU1Vv.Xswg$G8WJKZQ3RW0g1Or4KYkWcW3wFjTgUiXUvW6QaMyMI10',
            role: 'admin', contact: '1234567890'
        })
        """)

        session.write_transaction(run_query, """
        // Create Supplier
        CREATE (:User {
            id: '2', name: 'Supplier One', email: 'supplier@example.com',
            password: '$pbkdf2-sha256$29000$KtF6W3BhWh9KQU1Vv.Xswg$G8WJKZQ3RW0g1Or4KYkWcW3wFjTgUiXUvW6QaMyMI10',
            role: 'supplier', contact: '9876543210'
        })
        """)

        session.write_transaction(run_query, """
        // Create Consumer
        CREATE (:User {
            id: '3', name: 'Consumer One', email: 'consumer@example.com',
            password: '$pbkdf2-sha256$29000$KtF6W3BhWh9KQU1Vv.Xswg$G8WJKZQ3RW0g1Or4KYkWcW3wFjTgUiXUvW6QaMyMI10',
            role: 'consumer', contact: '9998887770'
        })
        """)

        session.write_transaction(run_query, """
        // Create Category and Brand
        CREATE (c:Category {id: 'cat1', name: 'Operating System'})
        CREATE (b:Brand {id: 'brand1', name: 'TechCorp'})
        """)

        session.write_transaction(run_query, """
        // Create Product and link to Category, Brand, Supplier
        MATCH (s:User {id: '2'}), (c:Category {id: 'cat1'}), (b:Brand {id: 'brand1'})
        CREATE (p:Product {
            id: 'prod1', name: 'TechOS', description: 'A modern OS',
            cost: 99.99, version: '1.0'
        })
        CREATE (s)-[:SUPPLIES]->(p)
        CREATE (p)-[:BELONGS_TO]->(c)
        CREATE (p)-[:BRANDED_BY]->(b)
        """)

        session.write_transaction(run_query, """
        // Create Subproduct
        MATCH (p:Product {id: 'prod1'})
        CREATE (sp:SubProduct {
            id: 'sub1', name: 'TechOS Lite', version: '1.0-lite',
            description: 'Lightweight version of TechOS'
        })
        CREATE (sp)-[:SUBPART_OF]->(p)
        """)

        session.write_transaction(run_query, """
        // Create Purchase
        MATCH (u:User {id: '3'}), (p:Product {id: 'prod1'})
        CREATE (u)-[:PURCHASED {timestamp: datetime()}]->(p)
        """)

        print("✅ Neo4j database initialized with sample data.")

if __name__ == "__main__":
    init_data()
