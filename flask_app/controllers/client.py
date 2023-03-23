from flask import Flask, render_template, request, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.client_model import Client

@app.route('/employee/add_client', methods=['POST'])
def add_client():
    if not Client.validate_client(request.form):
        return redirect('/employee/home')
    new_client = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    Client.create_client(new_client)
    flash('Client added successfully', 'client_added')
    return redirect('/employee/home')