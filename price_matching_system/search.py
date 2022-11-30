
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from datetime import datetime

from price_matching_system.db import get_conn

bp = Blueprint("search", __name__)

@bp.route('/')
@bp.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@bp.post("/search")
def SearchProduct():

    if "search-input" in request.form:
        search_string = (request.form["search-input"])
    else:
        search_string = ''
    print(search_string)

    conn = get_conn()
    cursor = conn.cursor()

    query = f""" SELECT 
            ProductDetailId
            , ProductName
            , Model
            , Year
            , Storage
            , SourceName
            , CAST(Price AS INT) AS Price
			, (CASE WHEN UserId IS NULL THEN 0 ELSE 1 END) AS IsBookmark
            FROM
            (
	            SELECT pd.ProductDetailId
	            , p.ProductName
	            , pd.Model
	            , pd.Year
	            , pd.Storage
	            , s.SourceName
	            , prd.Price
				, ub.UserId
	            , ROW_NUMBER() OVER (PARTITION BY pd.ProductDetailId ORDER BY PriceDetailDate DESC, Price) AS rownum
	            FROM dbo.tbl_Product p
	            INNER JOIN tbl_ProductDetail pd
	            ON p.ProductId = pd.ProductId
	            INNER JOIN tbl_PriceDetail prd
	            ON pd.ProductDetailId = prd.ProductDetailId
	            INNER JOIN tbl_Source s
	            ON prd.SourceId = s.SourceId
				LEFT JOIN tbl_UserBookmark ub
				ON ub.ProductDetailId = pd.ProductDetailId AND ub.UserId = {0 if g.user is None else g.user.get('UserId', 0)}
            ) temp
            WHERE rownum = 1
            AND ProductName LIKE """ + f"'%{search_string}%'"
    print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    print(results)

    return render_template(
        'index.html',
        results = results
    )