from flask import Flask, render_template, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.invoice_model import Invoice
from flask_app.models.product_model import Product

from datetime import date

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
    print("total price: ",  total_price)
    
    
    # Creating a new invoice and then it is adding it to the database.
    new_invoice = {
        'amount': total_price,
        'tax': 8.25,
        'date_due': date.today(),
        'date_paid': date.today(),
        'clients_email': session['client_email']
    }
    invoice = Invoice.create_invoice(new_invoice)
    print(invoice, "invoice created")
    
    this_id = {
        'id': invoice
    }
    
    invoice = Invoice.get_invoice_by_id(this_id)
    
    # Creating a relationship between the invoice and the product.
    for item in session['buying']:
        invoice_product_relationship = {
            'invoice_id': invoice.id,
            'date_due': invoice.date_due,
            'clients_email': session['client_email'],
            'product_id': item
        }
        Invoice.create_invoice_product_relationship(invoice_product_relationship)
        
    return render_template('checkout_page.html', list_of_products=list_of_products, total_price=total_price)