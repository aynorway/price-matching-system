"""
The flask application package.
"""

import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
DRIVER = os.environ.get('DRIVER', 'SQL Server')
SERVER_NAME = os.environ.get('SERVER_NAME', '')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'PriceMatchingSystem')

app.config.from_mapping(
    CONN_STRING = f'Driver={{{DRIVER}}};Server={SERVER_NAME};Database={DATABASE_NAME};Trust_Connection=yes;'    
)

from price_matching_system import db
db.init_app(app)

from price_matching_system import user
app.register_blueprint(user.bp)

import price_matching_system.views
