from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.payment_method_model import Payment_Method

@app.route('/payment_method', methods=['POST'])
def payment_method():
    this_email = {
        'email': session['client_email']
    }
    current_client = Client.get_client_by_email(this_email)
    new_card = {
        'card_number': request.form['card_number'],
        'expiration_date': request.form['expiration_date'],
        'CVC': request.form['CVC'],
        'clients_email': session['client_email'],
        'clients_id': current_client.id
    }
    Payment_Method.create_payment_method(new_card)
    