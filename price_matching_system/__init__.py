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
        CONN_STRING = f'Driver={{{DRIVER}}};Server={SERVER_NAME};Database={DATABASE_NAME};Trust_Connection=yes;'    
    )

    app.secret_key = b'_5#y2L"F4Qadsadsf8z\n\xec]/'

    from price_matching_system import db
    db.init_app(app)

    from price_matching_system import search
    app.register_blueprint(search.bp)

    from price_matching_system import login
    app.register_blueprint(login.bp)

    app.add_url_rule("/", endpoint="home")

    return app
