
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from price_matching_system.db import get_conn

bp = Blueprint("search", __name__)

@bp.post("/search")
def SearchProduct():

    if "search-input" in request.form:
        search_string = (request.form["search-input"])
    else:
        search_string = ''
    print(search_string)

    conn = get_conn()
    cursor = conn.cursor()
    query = "SELECT * FROM tbl_Product WHERE ProductName LIKE " + f"'%{search_string}%'"
    print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    print(results)

    return render_template(
        'index.html',
        search_results = results
    )