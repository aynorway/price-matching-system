

from flask import g
from flask import current_app
import pyodbc

def get_conn():
    if "conn" not in g:
        g.conn = pyodbc.connect(current_app.config['CONN_STRING'])
    return g.conn

def close_conn(e = None):
    conn = g.pop("conn", None)
    if conn is not None:
        conn.close()

def init_app(app):
    '''
    When Request ends, close the db connection
    '''
    app.teardown_appcontext(close_conn)