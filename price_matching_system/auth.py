
import functools
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import pyodbc

from price_matching_system.db import get_conn

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("login_id")

    if user_id is None:
        g.user = None
    else:
        try:
            conn = get_conn()
            cursor = conn.cursor()
            query = f"""SELECT l.Email, u.UserName, l.LoginId, u.UserId 
                        FROM dbo.tbl_Login l
                        INNER JOIN dbo.tbl_User u
                        ON l.UserId = u.UserId
                        WHERE LoginId =  {session.get('login_id')}"""
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            user = dict(zip(columns, row))
            g.user = user
            print('loaded user object in g')
        except:
            g.user = None

@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        email = request.form["email"]

        conn = get_conn()
        cursor = conn.cursor()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "Email is required."
        elif password != repeat_password:
            error = "Passwords don't match."

        if error is None:
            try:
                query = f"INSERT INTO dbo.tbl_User(Username) VALUES('{username}')"
                cursor.execute(query)

                query = "SELECT SCOPE_IDENTITY()"
                cursor.execute(query)
                user_id = cursor.fetchone()[0]

                query= f"INSERT INTO dbo.tbl_Login VALUES ('{email}', '{generate_password_hash(password)}', {user_id})"
                cursor.execute(query)
                cursor.commit()
            except pyodbc.Error as ex:
                sqlstate = ex.args[0]
                print(ex)
                print(sqlstate)
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                if sqlstate == '23000':
                    error = f"Email {email} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_conn()
        cursor = conn.cursor()
        error = None

        query = f"SELECT * FROM dbo.tbl_Login WHERE Email = '{email}'"

        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row is not None:
            login = dict(zip(columns, row))
        else:
            login = None

        if login is None:
            error = "Incorrect Email."
        elif not check_password_hash(login["Password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["login_id"] = login["LoginId"]
            return redirect(url_for("home"))

        flash(error)

    return render_template("auth/login.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home"))