from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.product_model import Product


@app.route('/client/<int:id>')
def display_client_products(id):
    list_of_products = Product.get_product_by_client(id)
    return render_template('client.html', list_of_products=list_of_products)