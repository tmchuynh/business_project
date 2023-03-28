from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.payment_method_model import Payment_Method
from flask_app.models.client_model import Client

@app.route('/payment_method', methods=['POST'])
def payment_method():
    """
    This function takes the information from the payment method form and validates it. If it is valid,
    it creates a new payment method in the database
    :return: The payment method is being returned.
    """
    this_email = {
        'email': session['client_email']
    }
    current_client = Client.get_client_by_email(this_email)
    if not Payment_Method.validate_payment_method(request.form):
        return redirect('/invoice')

    client_email = {
        'email': session['client_email']
    }
    if Client.check_database(client_email):
        new_card = {
            'card_number': int(request.form['card_number']),
            'expiration_date': request.form['expiration_date'],
            'CVC': int(request.form['CVC']),
            'clients_email': session['client_email'],
            'clients_id': current_client.id
        }
        Payment_Method.create_payment_method(new_card)
    return redirect('/payment_method')