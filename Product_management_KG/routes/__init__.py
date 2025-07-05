from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .consumer_routes import consumer_bp
from .supplier_routes import supplier_bp
from .product_routes import product_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(consumer_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)
