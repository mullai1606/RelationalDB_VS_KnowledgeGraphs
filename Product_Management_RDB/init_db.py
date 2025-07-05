from app import create_app, db
from models.user import User
from models.role import Role 
app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
