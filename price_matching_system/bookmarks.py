
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask import jsonify

from price_matching_system.db import get_conn
from price_matching_system.auth import login_required

bp = Blueprint("bookmarks", __name__)

@bp.route("/bookmarks", methods=["GET"])
@login_required
def view_bookmarks_page():

    conn = get_conn()
    cursor = conn.cursor()

    query = f"""
            SELECT 
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
				INNER JOIN tbl_UserBookmark ub
				ON ub.ProductDetailId = pd.ProductDetailId AND ub.UserId = {g.user['UserId']}
            ) temp
            WHERE rownum = 1"""

    print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    print(results)

    return render_template(
        "bookmarks.html",
        title="My Bookmarks",
        results = results
    )


@bp.route("/bookmark/<int:product_detail_id>", methods=["POST"])
@login_required
def bookmark_product(product_detail_id):
    """
    Bookmark a Product
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()

        query = f"INSERT INTO dbo.tbl_UserBookmark VALUES ({g.user['UserId']}, {product_detail_id})"
        cursor.execute(query)

        cursor.commit()

        return jsonify({"message": "Success"})
    except:
        return jsonify({"message": "Failed"})


@bp.route("/bookmark/<int:product_detail_id>", methods=["DELETE"])
@login_required
def remove_bookmark_product(product_detail_id):
    """
    Delete a Bookmark for Product
    """
    try:
        conn = get_conn()
        cursor = conn.cursor()

        query = f"DELETE FROM dbo.tbl_UserBookmark WHERE UserId = {g.user['UserId']} AND ProductDetailId = {product_detail_id}"
        cursor.execute(query)

        cursor.commit()

        return jsonify({"message": "Success"})
    except:
        return jsonify({"message": "Failed"})