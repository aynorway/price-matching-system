
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from price_matching_system.db import get_conn

bp = Blueprint("user", __name__)

@bp.route("/user")
def UserDetails():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM UserTable')
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results