from flask import Flask, render_template, request, redirect, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.client_model import Client
from flask_app.models.employee_model import Employee

@app.route('/employee/add_client', methods=['POST'])
def add_client():
    """
    The function creates a new client and then creates a relationship between the new client and the
    employee who created the client
    :return: The redirect is returning the employee's home page.
    """
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
    """
    It gets all the clients from the database and renders the employee_home.html template with the list
    of clients
    :return: A list of all clients
    """
    this_employee = {
        'employee_id': session['employee_id'],
    }
    client_object = Employee.get_client_by_employee(this_employee)
    print(client_object)
    return render_template('employee_home.html', client_object=client_object)