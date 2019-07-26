from flask import Flask, render_template, request, redirect, session, flash, get_flashed_messages
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from datetime import datetime
import re
import my_utils
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'darksecret'

dbname = 'eCommerce_db'
# The following queries can be re-used or edited before use
# CRUD - Create, Read, Update, Delete
CREATE_RECORD = 'INSERT INTO table ( col1, col2, created_at, updated_at ) VALUES ( %(col1)s, %(col2)s, NOW(), NOW() )'
READ_ALL      = 'SELECT * from table'
READ_ONE      = 'SELECT * from table WHERE id=%(id)s'
UPDATE_RECORD = 'UPDATE table SET col1=%(col1)s, col2=%(col2)s, updated_at=NOW() WHERE id=%(id)s'
DELETE_RECORD = 'DELETE FROM table WHERE id=%(id)s'

products = [{'name':'Prince Racquet', 'id':1, 'image_id': 'prince_racquet'}, {'name': 'Wilson Racquet', 'id':2, 'image_id':'wilson_racquet'}, {'name': 'Head Racquet', 'id':3, 'image_id': 'head_racquet'}, {'name': 'Babolat Racquet', 'id':4, 'image_id': 'babolat_racquet'}]
# categories = [{'name':'T-shirts', 'id':1}, {'name': 'Shoes', 'id':2}, {'name': 'Racquets', 'id':3}]

@app.route("/products/category/<catid>/<pagenum>")
def mainpage(catid, pagenum):

    mysql = connectToMySQL(dbname)
    categories = mysql.query_db("SELECT * FROM categories")
    mysql = connectToMySQL(dbname)
    products = mysql.query_db("SELECT * FROM products")


    return render_template('index.html', catid=int(catid), pagenum=int(pagenum), categories=categories, products=products)

@app.route("/process_search", methods=["POST"])
def process_search():
    return redirect("/products/category/1/1")

@app.route('/carts')
def carts():
    return render_template('carts.html')

@app.route("/products/show/<productid>")
def display_product(productid):
    mysql = connectToMySQL(dbname)
    query = f"SELECT * FROM products WHERE id = {productid};"
    product = mysql.query_db(query)
    product = product[0]
    return render_template('view_product.html', product=product, productid=productid)

@app.route("/add_to_cart/<id>", methods=['POST'])
def add_to_cart(id):
    flash("Item added to cart", "success")
    return redirect("/products/show/"+id)

@app.route("/process_cart", methods=['POST'])
def process_cart():
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO customers (first_name, last_name) VALUES ( %(firstname)s, %(lastname)s)"
    data = {
        "firstname": request.form['firstname'],
        "lastname": request.form['lastname']
    }
    customer_id = mysql.query_db(query, data)
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO billing_address (address, address_2, city, state, zip_code) values ( %(address)s, %(address2)s, %(city)s, %(state)s, %(zipcode)s)"
    data = {
        "address": request.form['address'],
        "address2": request.form['address2'],
        "city": request.form['city'],
        "state": request.form['state'],
        "zipcode": request.form['zipcode']
    }
    billing_address_id = mysql.query_db(query, data)
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO shipping_address (address, address_2, city, state, zip_code) values ( %(address)s, %(address2)s, %(city)s, %(state)s, %(zipcode)s)"
    data = {
        "address": request.form['bill_address'],
        "address2": request.form['bill_address2'],
        "city": request.form['bill_city'],
        "state": request.form['bill_state'],
        "zipcode": request.form['bill_zipcode']
    }
    shipping_address_id = mysql.query_db(query, data)
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO payment (card, security_code) values (%(card)s, %(cvv)s)"
    data = {
        "card": request.form['card'],
        "cvv": request.form['cvv']
    }
    payment_id = mysql.query_db(query, data)
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO orders (customer_id, shipping_address_id, billing_address_id, payment_id) VALUES (%(customer_id)s, %(shipping_address_id)s, %(billing_address_id)s, %(payment_id)s)"; 
    
    data = {
        "customer_id": customer_id,
        "shipping_address_id": shipping_address_id,
        "billing_address_id": billing_address_id,
        "payment_id": payment_id
    }
    order_id = mysql.query_db(query, data)
    return redirect("/carts")


@app.route('/admin')
def display_admin_login():
    return render_template('admin.html')
    


@app.route('/admin_login', methods=["POST"])
def admin_login():
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO admins (email, password) VALUES ( %(email)s, %(password)s );"
    admins = mysql.query_db(query, request.form)
    return redirect('/dashboard/orders')

@app.route('/dashboard/orders')
def orders_page():
    mysql = connectToMySQL(dbname)
    query =  "select orders.id, first_name, created_at, address from customers join orders on customers.id = orders.customer_id join billing_address on billing_address.id = orders.billing_address_id;"
    orders = mysql.query_db(query)
    return render_template('all_orders.html', orders=orders)


@app.route('/dashboard/products')
def products_page():
    mysql = connectToMySQL(dbname)
    all_products = mysql.query_db('SELECT * FROM products;')
    return render_template('all_products.html', all_products = all_products)

@app.route('/add_product', methods=["POST"])
def add_product():
    mysql = connectToMySQL(dbname)
    category_id = mysql.query_db(f"SELECT id FROM categories WHERE name = '{request.form['category']}'")
    category_id = category_id[0]['id']
    mysql = connectToMySQL(dbname)
    query = "INSERT INTO products (name, inventory_count, quantity_sold, product_image, price, categories_id, description) VALUES (%(name)s, %(inventory_count)s, %(quantity_sold)s, %(product_image)s, %(price)s, %(categories_id)s, %(description)s);"
    data = {
        "name": request.form['name'],   
        "product_image": request.form['pic'],
        "categories_id": category_id,
        "description": request.form['description'],
        "inventory_count": 10,
        "quantity_sold": 0,
        "price": 20.00

    }
    new_product_id = mysql.query_db(query, data)
    print(new_product_id)
    return redirect('/dashboard/products')

@app.route('/edit_product', methods=["POST"])
def edit_product():
    return redirect('/dashboard/products')




@app.route('/show_order')
def show_order():
    return render_template('order.html')


@app.route('/log_off')
def destroy_session():
    session.clear()
    return redirect('/admin')



if __name__ == "__main__":
    app.run(debug=True)
