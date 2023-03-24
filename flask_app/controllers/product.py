from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.product_model import Product
from flask_app.models.client_model import Client


@app.route('/client/<int:id>')
def display_client_products(id):
    this_client = {
        'client_id': id,
    }
    current_client = Client.get_client_by_id(this_client)
    print(current_client)
    list_of_products = Client.get_product_by_client(this_client)
    return render_template('client_products.html', list_of_products=list_of_products, current_client=current_client)