from flask import Flask, redirect, url_for
from config import Config
from extensions import init_neo4j
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.consumer_routes import consumer_bp
from routes.supplier_routes import supplier_bp
from routes.product_routes import product_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_neo4j(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(consumer_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)

    # 👇 Add root route to redirect to login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
