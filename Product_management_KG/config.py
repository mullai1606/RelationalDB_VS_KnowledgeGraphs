import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
#     NEO4J_URI = "bolt://localhost:7687"
#     NEO4J_USERNAME = "neo4j"
#     NEO4J_PASSWORD = "00000000"  # Replace with your actual password

class Config:
    SECRET_KEY = 'your-secret-key'
    NEO4J_URI = 'bolt://localhost:7687'
    NEO4J_USERNAME = 'neo4j'
    NEO4J_PASSWORD = '00000000'