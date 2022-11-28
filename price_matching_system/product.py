
from ast import Lambda
from this import s
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from datetime import date, datetime, timedelta

from price_matching_system.db import get_conn

bp = Blueprint("product", __name__)

@bp.route("/product/<int:product_detail_id>", methods=["GET"])
def show_product_page(product_detail_id):

    print(product_detail_id)

    conn = get_conn()
    cursor = conn.cursor()

    query = f"""
        SELECT TOP 100 pcd.PriceDetailDate
        , CAST(Price AS INT) AS Price
        , s.SourceName
        FROM dbo.tbl_Product p
        INNER JOIN tbl_ProductDetail prd
        ON p.ProductId = prd.ProductId
        INNER JOIN tbl_PriceDetail pcd
        ON prd.ProductDetailId = pcd.ProductDetailId
        INNER JOIN tbl_Source s
        ON pcd.SourceId = s.SourceId
        WHERE prd.ProductDetailId = {product_detail_id}
        ORDER BY pcd.PriceDetailDate DESC"""

    print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    print(results)

    query = f"""
        SELECT ProductName, Model, Year, Storage
        FROM dbo.tbl_Product p
        INNER JOIN tbl_ProductDetail prd
        ON p.ProductId = prd.ProductId
        WHERE prd.ProductDetailId = {product_detail_id}
        """

    print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    row = cursor.fetchone()
    product_data = dict(zip(columns, row))
    print(product_data)

    query = f"""
        SELECT CAST(Price AS INT) AS Price, s.SourceName
        FROM tbl_PriceDetail pcd
        INNER JOIN tbl_Source s
        ON pcd.SourceId = s.SourceId
        WHERE pcd.ProductDetailId = {product_detail_id}
        AND pcd.PriceDetailDate = (SELECT MAX(PriceDetailDate) From tbl_PriceDetail WHERE ProductDetailId = {product_detail_id})
    """
    print(query)
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    latest_price_data = []
    for row in cursor.fetchall():
        latest_price_data.append(dict(zip(columns, row)))
    print(latest_price_data)

    unique_sources = set(result['SourceName'] for result in results)
    
    chart_data = {}
    for source in unique_sources:
        chart_data[source] = {}
        chart_data[source]['price'] = []
        chart_data[source]['date'] = []
        for result in filter(lambda x: x['SourceName'] == source, reversed(results)):
            chart_data[source]['price'].append(result['Price'])
            chart_data[source]['date'].append(result['PriceDetailDate'])

    print(chart_data)

    stat_data = {}
    stat_data['lowest_price'] = results[0]['Price']
    stat_data['lowest_price_date'] = results[0]['PriceDetailDate']
    stat_data['lowest_price_source'] = results[0]['SourceName']
    for result in results:
        if result['Price'] < stat_data['lowest_price']:
            stat_data['lowest_price'] = result['Price']
            stat_data['lowest_price_date'] = result['PriceDetailDate']
            stat_data['lowest_price_source'] = result['SourceName']

    return render_template(
        "product.html",
        title="Product Details",
        product_data = product_data,
        latest_price_data = latest_price_data,
        chart_data = chart_data,
        stat_data = stat_data
    )