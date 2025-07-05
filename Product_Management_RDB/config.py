# import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'this_is_a_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///product_mgmt.db'  # Use MySQL or PostgreSQL for production
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/product_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

