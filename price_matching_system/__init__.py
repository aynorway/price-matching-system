"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import price_matching_system.views
