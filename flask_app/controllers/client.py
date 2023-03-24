from flask import Flask, render_template, request, redirect, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.client_model import Client
from flask_app.models.employee_model import Employee
from flask_app.models.product_model import Product

@app.route('/clients')
def display_product():
    list_of_products = Product.get_all_products()
    return render_template('display_all_products.html', list_of_products=list_of_products)


@app.route('/clients/options')
def show_client_options():
    if 'client_email' not in session:
        return render_template('create_client.html')
    return render_template('cart.html')


@app.route('/clients/login', methods=['POST'])
def check_for_client_in_database():
    if not Client.validate_client_login(request.form):
        return redirect('/clients/options')
    session['client_email'] = request.form['email']
    return redirect('/clients')


@app.route('/clients/register', methods=['GET', 'POST'])
def register_client():
    if 'client_email' not in session:
        if not Client.validate_client(request.form):
            return redirect('/clients/options')
        new_client = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email']
        }
        Client.create_client(new_client)
        flash('You have successfully registered!', 'client_success')
        print(new_client['email'])
        session['client_email'] = new_client['email']
        print(session['client_email'])
        return redirect('/clients')
    return render_template('cart.html')

@app.route('/employee/add_client', methods=['POST'])
def add_client():
    """
    The function creates a new client and then creates a relationship between the new client and the
    employee who created the client
    :return: The redirect is returning the employee's home page.
    """
    if not Client.validate_client(request.form):
        return redirect('/employee/get_clients')
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