from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.invoice_model import Invoice
from flask_app.models.client_model import Client
from flask_app.models.product_model import Product


@app.route('/client/<int:id>')
def display_client_products(id):
    """
    This function takes in a client id and returns a list of products that belong to that client
    
    :param id: the id of the client
    :return: A list of products that are associated with the client.
    """
    this_client = {
        'client_id': id,
    }
    session['client_id'] = id
    current_client = Client.get_client_by_id(this_client)
    this_client = {
        'client_email': current_client.email
    }
    print("current client ", current_client)
    list_of_invoices = Invoice.get_current_product_by_client(this_client)
    for invoice in list_of_invoices:
        print("status ", invoice['status'])
    
    
    return render_template('client_products.html', list_of_invoices=list_of_invoices, current_client=current_client)


@app.route('/client/update_status/<int:invoice_id>', methods=['POST'])
def update_product_status(invoice_id):
    """
    The function takes the invoice_id as an argument, and then updates the invoice with the new
    information from the form
    
    :param invoice_id: the id of the invoice that is being updated
    :return: the redirect to the client page.
    """
    print(request.form)
    this_invoice = {
        'amount': request.form['amount'],
        'invoice_id': invoice_id
    }
    Invoice.update_invoice(this_invoice)
    
    this_product = {
        'status': request.form['status']
    }
    Product.update_product_status(this_product)
    flash('Product updated', 'product_updated')
    return redirect(f"/client/{session['client_id']}")
    