from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from datetime import date, datetime, timedelta
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import pyodbc

from price_matching_system.db import get_conn

bp = Blueprint("user", __name__)

@bp.route("/user")
def user():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """

    conn = get_conn()
    cursor = conn.cursor()
    query = f"""SELECT * FROM dbo.tbl_User u
                    WHERE UserId = {session.get('login_id')}"""
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()
    personalInfo = dict(zip(columns, row))

    return render_template("user.html", personalInfo = personalInfo)

@bp.route("/userEdit")
def userEdit():
    conn = get_conn()
    cursor = conn.cursor()
    query = f"""SELECT * FROM dbo.tbl_User u
                        WHERE UserId = {session.get('login_id')}"""
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()
    personalInfo = dict(zip(columns, row))

    return render_template("user_edit.html", personalInfo=personalInfo)


@bp.route("/userSave", methods=("GET", "POST"))
def userSave():
    FirstName = request.form["FirstName"]
    LastName = request.form["LastName"]
    Address1 = request.form["Address1"]
    Address2 = request.form["Address2"]
    City = request.form["City"]
    Province = request.form["Province"]
    Country = request.form["Country"]
    PostalCode = request.form["PostalCode"]
    Phone = request.form["Phone"]

    conn = get_conn()
    cursor = conn.cursor()
    error = None

    if error is None:
        try:
            query = f"UPDATE dbo.tbl_User SET [FirstName] = ? " \
                    f",[LastName] = ? " \
                    f",[Address1] = ? " \
                    f",[Address2] = ? " \
                    f",[City] = ? " \
                    f",[Province] = ? " \
                    f",[Country] = ? " \
                    f",[PostalCode] = ? " \
                    f",[Phone] = ? " \
                    f"WHERE UserId = {session.get('login_id')}"
            print(query)
            cursor.execute(query, FirstName, LastName, Address1, Address2, City, Province, Country, PostalCode, Phone)
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(ex)
            print(sqlstate)
        else:
            # Success, go to the login page.
            return redirect(url_for("user.user"))

    flash(error)

    return redirect(url_for("user.user"))