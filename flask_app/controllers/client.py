from flask import Flask, render_template, request, redirect, flash, session
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
    current_client = Client.get_client_by_email(new_client)
    print(current_client)
    relationship = {
        'client_id': current_client.id,
        'client_email': current_client.email,
        'employee_id': session['employee_id'],
        'employee_email': session['email']
    }
    Client.create_relationship_with_employee(relationship)
    # updates the list of the employee's clients before they add a new client ( same page )
    return redirect('/employee/get_clients')

@app.route('/employee/get_clients', methods=['GET'])
def get_clients():
    list_of_clients = Client.get_all_clients()
    return render_template('employee_home.html', list_of_clients=list_of_clients)