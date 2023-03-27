from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.invoice_model import Invoice
from flask_app.models.client_model import Client
from flask_app.models.product_model import Product

@app.route('/invoice')
def show_invoice():
    """
    It takes the list of products in the session, and then it loops through each product, and then it
    gets the product from the database, and then it adds the price of the product to the total price,
    and then it adds the product to a list of products, and then it renders the checkout page with the
    list of products and the total price.
    :return: A list of products and the total price
    """
    list_of_products = []
    total_price = 0
    
    print(session['buying'])
    
    for item in session['buying']:
        this_item = {
            'product_id': item
        }
        this_product = Product.get_product_by_id(this_item)
        
        total_price += (this_product.price - (this_product.price * this_product.discount))
        
        list_of_products.append(this_product)
    print(list_of_products)
    return render_template('checkout_page.html', list_of_products=list_of_products, total_price=total_price)