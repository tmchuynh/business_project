from flask import Flask, render_template, request, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.employee_model import Employee
from flask_app.models.product_model import Product
from flask_app.models.client_model import Client
import random, string

@app.route('/admin')
def admin():
    """
    It gets all the employees from the database and passes them to the admin.html template
    :return: A list of all employees
    """
    list_of_employees = Employee.get_all_employees()
    list_of_products = Product.get_all_products()
    list_of_clients = Client.get_all_clients()
    return render_template('admin.html', list_of_employees=list_of_employees, list_of_products=list_of_products, list_of_clients=list_of_clients)


@app.route('/admin/add_employee', methods=['POST'])
def add_employee():
    """
    We create a random password, hash it, and store it in the database
    :return: a redirect to the admin page.
    """
    if not Employee.validate_employee_form_on_creation(request.form):
        return redirect('/admin')
    
    # when an employee is first created, the password is randomly generated
    temp = string.ascii_lowercase + string.ascii_uppercase + string.digits
    temp_password = ''.join(random.choice(temp) for i in range(8))
    print(temp_password)
    
    new_employee = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(temp_password).decode('utf-8'),
        'temp_password': temp_password
    }
    
    Employee.create_employee(new_employee)
    flash('Employee added successfully', 'employee_added')
    return redirect('/admin')


@app.route('/admin/edit_employee_form/<int:employee_id>')
def edit_employee_form(employee_id):
    this_employee = {
        'employee_id': employee_id
    }
    employee = Employee.get_employee_by_id(this_employee)
    list_of_employees = Employee.get_all_employees()
    list_of_products = Product.get_all_products()
    list_of_clients = Client.get_all_clients()
    return render_template('admin_edit_employee_form.html', list_of_clients=list_of_clients, list_of_products=list_of_products, list_of_employees=list_of_employees, employee=employee)


@app.route('/admin/edit_employee/<int:employee_id>', methods=['POST'])
def edit_employee(employee_id):
    if not Employee.validate_employee_form_on_creation(request.form):
        return redirect(f'/admin/edit_employee_form/{employee_id}')
    this_employee = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    Employee.admin_update_employee(this_employee)
    flash('Employee updated successfully', 'employee_updated')
    return redirect('/admin')


@app.route('/admin/delete_employee/<int:employee_id>')
def delete_employee(employee_id):
    this_employee = {
        'employee_id': employee_id
    }
    Employee.delete_employee(this_employee)
    return redirect('/admin')


@app.route('/admin/add_product', methods=['POST'])
def add_product():
    """
    We're creating a new product and adding it to the database
    :return: a redirect to the admin page.
    """
    if not Product.validate_product_form_on_creation(request.form):
        return redirect('/admin')
    
    new_product = {
        'name': request.form['name'],
        'category': request.form['category'],
        'price': request.form['price']
    }
    Product.create_product(new_product)
    flash('Product added successfully', 'product_added')
    return redirect('/admin')