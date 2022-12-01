from turtle import title
from unicodedata import category
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
import re

from price_matching_system.db import get_conn
from price_matching_system.auth import login_required

bp = Blueprint("user", __name__)

def getPersonalInfo():
    conn = get_conn()
    cursor = conn.cursor()
    query = f"""SELECT * FROM dbo.tbl_User u
                            WHERE UserId = {g.user['UserId']}"""
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()
    personalInfo = dict(zip(columns, row))
    return personalInfo

@bp.route("/user", methods=("GET", "POST"))
@login_required
def user():
    """After user login.
    Allow user to change the person information.
    Submit button allows user to save and back to user page.
    """
    if request.method == "GET":
        return render_template("user.html", personalInfo = getPersonalInfo(), title="Profile")

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
                    f"WHERE UserId = {g.user['UserId']}"
            print(query)
            cursor.execute(query, FirstName, LastName, Address1, Address2, City, Province, Country, PostalCode, Phone)
            cursor.commit()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print(ex)
            print(sqlstate)
        else:
            # Success, go to the user page.
            return redirect(url_for("user.user"))

    flash(error)

    return redirect(url_for("user.user"))



@bp.route("/user/edit")
@login_required
def userEdit():
    return render_template("user_edit.html", personalInfo=getPersonalInfo(), title="Edit Profile")

@bp.route("/user/change_password", methods=["POST"])
@login_required
def change_user_password():
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    repeat_new_password = request.form["repeat_new_password"]

    conn = get_conn()
    cursor = conn.cursor()
    error = None

    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pat = re.compile(reg)

    if not current_password:
        error = "Username is required."
    elif not new_password:
        error = "Password is required."
    elif not repeat_new_password:
        error = "Email is required."
    elif new_password != repeat_new_password:
        error = "Passwords don't match."
    elif not re.search(pat, new_password):
            error = "Password should be 6 to 20 characters in length with atleast one digit, lower case, upper case and special character."

    if error is None:
        try:
            query = f"SELECT * FROM dbo.tbl_Login WHERE LoginId = {g.user['LoginId']}"

            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            if row is not None:
                login = dict(zip(columns, row))
            else:
                login = None

            if login is None:
                error = "Not logged-in"
            elif not check_password_hash(login["Password"], current_password):
                error = "Incorrect password."
            else:
                query = f"UPDATE dbo.tbl_Login SET Password = '{generate_password_hash(new_password)}' WHERE LoginId = {g.user['LoginId']}"
                cursor.execute(query)
                cursor.commit()
        except:
            error = "Could not update password"
    
    if error is None:
        flash("Password Changed Successfully", category = "info")
    else:
        flash(error)
    return redirect(url_for("user.userEdit"))