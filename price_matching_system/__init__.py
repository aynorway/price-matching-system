"""
The flask application package.
"""

import os
from flask import Flask
from dotenv import load_dotenv

def create_app(config=None):
    app = Flask(__name__)

    load_dotenv()
    DRIVER = os.environ.get('DRIVER', 'SQL Server')
    SERVER_NAME = os.environ.get('SERVER_NAME', '')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'PriceMatchingSystem')

    app.config.from_mapping(
        SECRET_KEY="dev",
        CONN_STRING = f'Driver={{{DRIVER}}};Server={SERVER_NAME};Database={DATABASE_NAME};Trust_Connection=yes;'    
    )

    from price_matching_system import db
    db.init_app(app)

    from price_matching_system import search
    from price_matching_system import product
    from price_matching_system import auth
    from price_matching_system import user
    from price_matching_system import bookmarks
    
    app.register_blueprint(search.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(bookmarks.bp)

    app.add_url_rule("/", endpoint="home")

    return app