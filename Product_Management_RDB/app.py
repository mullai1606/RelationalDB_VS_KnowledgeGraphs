# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from config import Config

# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     login_manager.init_app(app)

#     # Import models to register them with SQLAlchemy
#     from models import product  # Add others like user, supplier as you implement them

#     # Register Blueprints (routes will be implemented later)
#     from routes.auth_routes import auth_bp
#     from routes.product_routes import product_bp
#     from routes.supplier_routes import supplier_bp
#     from routes.consumer_routes import consumer_bp
#     from routes.admin_routes import admin_bp

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(product_bp)
#     app.register_blueprint(supplier_bp)
#     app.register_blueprint(consumer_bp)
#     app.register_blueprint(admin_bp)

#     return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)


# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from config import Config

# db = SQLAlchemy()
# migrate = Migrate()
# login_manager = LoginManager()
# login_manager.login_view = "auth_bp.login"
# login_manager.login_message_category = "info"

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     db.init_app(app)
#     migrate.init_app(app, db)
#     login_manager.init_app(app)

#     # Import models to register with SQLAlchemy
#     from models import user, product, category, plant_brand, supplier

#     # Register blueprints
#     from routes.auth_routes import auth_bp
#     from routes.product_routes import product_bp
#     from routes.supplier_routes import supplier_bp
#     from routes.consumer_routes import consumer_bp
#     from routes.admin_routes import admin_bp

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(product_bp)
#     app.register_blueprint(supplier_bp)
#     app.register_blueprint(consumer_bp)
#     app.register_blueprint(admin_bp)

#     # Root route
#     @app.route("/")
#     def index():
#         return render_template("index.html")

#     return app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# from flask_migrate import Migrate
# from config import Config

# app = Flask(__name__)
# app.config.from_object(Config)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # Setup Flask-Login
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)

# from models.user import User  # Ensure this import is correct

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # Import models to register them with SQLAlchemy
# from models import user, product, category, plant_brand, supplier

# # Register blueprints
# from routes.auth_routes import auth_bp
# from routes.product_routes import product_bp
# from routes.supplier_routes import supplier_bp
# from routes.consumer_routes import consumer_bp
# from routes.admin_routes import admin_bp

# app.register_blueprint(auth_bp)
# app.register_blueprint(product_bp)
# app.register_blueprint(supplier_bp)
# app.register_blueprint(consumer_bp)
# app.register_blueprint(admin_bp)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Initialize extensions without app
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import models to register them with SQLAlchemy
    from models import user, product, category, plant_brand, supplier

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.product_routes import product_bp
    from routes.supplier_routes import supplier_bp
    from routes.consumer_routes import consumer_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(supplier_bp)
    app.register_blueprint(consumer_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


#run the app 

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

