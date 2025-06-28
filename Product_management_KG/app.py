# from flask import Flask, redirect, url_for
# from config import Config
# from extensions import init_neo4j

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     init_neo4j(app)

#     from routes.auth_routes import auth_bp
#     from routes.admin_routes import admin_bp
#     from routes.consumer_routes import consumer_bp
#     from routes.supplier_routes import supplier_bp
#     from routes.product_routes import product_bp


#     app.register_blueprint(auth_bp)
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(consumer_bp)
#     app.register_blueprint(supplier_bp)
#     app.register_blueprint(product_bp)

#     # 👇 Add root route to redirect to login
#     @app.route('/')
#     def index():
#         return redirect(url_for('auth.login'))

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)


from flask import Flask, render_template
from flask_login import LoginManager
from extensions import init_neo4j
from models.neo4j_user import load_user

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'

    app.config['NEO4J_URI'] = 'bolt://localhost:7687'
    app.config['NEO4J_USERNAME'] = 'neo4j'
    app.config['NEO4J_PASSWORD'] = '00000000'

    init_neo4j(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def user_loader(user_id):
        return load_user(user_id)

    from routes.auth_routes import auth_bp
    from routes.admin_routes import admin_bp
    from routes.consumer_routes import consumer_bp
    from routes.supplier_routes import supplier_bp
    from routes.product_routes import product_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(consumer_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(product_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

