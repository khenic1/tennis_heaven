from flask import Flask, render_template, request, redirect, session, flash, get_flashed_messages
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from datetime import datetime
import re
import my_utils
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'darksecret'

dbname = 'dbname'
# The following queries can be re-used or edited before use
# CRUD - Create, Read, Update, Delete
CREATE_RECORD = 'INSERT INTO table ( col1, col2, created_at, updated_at ) VALUES ( %(col1)s, %(col2)s, NOW(), NOW() )'
READ_ALL      = 'SELECT * from table'
READ_ONE      = 'SELECT * from table WHERE id=%(id)s'
UPDATE_RECORD = 'UPDATE table SET col1=%(col1)s, col2=%(col2)s, updated_at=NOW() WHERE id=%(id)s'
DELETE_RECORD = 'DELETE FROM table WHERE id=%(id)s'

products = [{'name':'Prince Racquet', 'id':1, 'image_id': 'prince_racquet'}, {'name': 'Wilson Racquet', 'id':2, 'image_id':'wilson_racquet'}, {'name': 'Head Racquet', 'id':3, 'image_id': 'head_racquet'}, {'name': 'Babolat Racquet', 'id':4, 'image_id': 'babolat_racquet'}]
categories = [{'name':'T-shirts', 'id':1}, {'name': 'Shoes', 'id':2}, {'name': 'Racquets', 'id':3}]

@app.route("/products/category/<catid>/<pagenum>")
def mainpage(catid, pagenum):
    #select query from categories, products, and images tables
    return render_template('index.html', catid=int(catid), pagenum=int(pagenum), categories=categories, products=products)

@app.route("/process_search", methods=["POST"])
def process_search():
    return redirect("/products/category/1/1")

@app.route("/carts")
def carts():
    return render_template('carts.html')

@app.route("/products/show/<productid>")
def display_product(productid):
    return render_template('view_product.html', productid=productid)

@app.route("/add_to_cart/<productid>", methods=['POST'])
def add_to_cart(productid):
    flash("Item added to cart", "success")
    return redirect("/products/show/"+productid)


@app.route('/admin')
def admin_login():
    return render_template('admin.html')

@app.route('/orders')
def orders_page():
    return render_template('all_orders.html')


@app.route('/products')
def products_page():
    return render_template('all_products.html')

@app.route('/show_order')
def show_order():
    return render_template('order.html')


if __name__ == "__main__":
    app.run(debug=True)
