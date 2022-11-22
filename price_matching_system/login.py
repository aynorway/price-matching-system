
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from datetime import datetime
from flask import session

from price_matching_system.db import get_conn

bp = Blueprint("login", __name__)

@bp.get("/login")
def loginPage():
    return render_template(
        'login.html'
    )

@bp.post("/doLogin")
def doLogin():

    # 1. receive username and password
    username = (request.form["username"])
    password = (request.form["password"])
    #print(username)
    #print(password)

    # 2. validate user
    conn = get_conn()
    cursor = conn.cursor()
    query = "SELECT * from dbo.tbl_Login WHERE Email=? AND Password=?"
    print(query)
    cursor.execute(query, username, password)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    print(results)

    # 2.1 if exist
    if len(results) > 0:
        print("exist")

        # 3. store id in session
        session['user'] = results[0]

        # 4. redirect to index page
        return redirect("/")

    # 2.2 not exist, username/pass not correct
    else:
        print("not exist")

        return redirect("/login")

@bp.get("/logout")
def logout():
    session.pop('user', None)
    return redirect("/")