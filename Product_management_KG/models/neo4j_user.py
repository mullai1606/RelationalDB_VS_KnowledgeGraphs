from flask_login import UserMixin

class Neo4jUser(UserMixin):
    def __init__(self, id, name, email, password, role, contact):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.contact = contact

    def get_id(self):
        return self.id
