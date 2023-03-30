from flask import Flask, render_template, request, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.employee_model import Employee
from flask_app.models.product_model import Product
from flask_app.models.client_model import Client
from flask_app.models.invoice_model import Invoice
import random, string

@app.route('/admin')
def admin():
    """
    It gets all the employees from the database and passes them to the admin.html template
    :return: A list of all employees
    """
    list_of_employees = Employee.get_all_employees()
    list_of_active_employees = Employee.get_active_employees()
    list_of_products = Product.get_all_products()
    list_of_clients = Client.get_all_clients()
    list_of_current_products = Invoice.get_current_products()
    return render_template('admin.html', list_of_employees=list_of_employees, list_of_active_employees=list_of_active_employees, list_of_products=list_of_products, list_of_clients=list_of_clients, list_of_current_products=list_of_current_products)


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
    temp_password = ''.join(random.choice(temp) for i in range(12))
    print("temp password ", temp_password)
    
    new_employee = {
        'first_name': request.form['first_name'].capitalize(),
        'last_name': request.form['last_name'].capitalize(),
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(temp_password).decode('utf-8'),
        'temp_password': temp_password
    }
    
    Employee.create_employee(new_employee)
    flash('Employee added successfully', 'employee_added')
    return redirect('/admin')


@app.route('/admin/edit_employee/<int:employee_id>', methods=['POST'])
def edit_employee(employee_id):
    """
    This function takes in an employee_id, validates the form data, updates the employee in the
    database, and redirects the user to the admin page.
    
    :param employee_id: the id of the employee to be updated
    :return: The employee_id, first_name, last_name, and email are being returned.
    """
    if not Employee.validate_employee_form_on_admin_update(request.form):
        return redirect(f'/admin')
    this_employee = {
        'employee_id': employee_id,
        'first_name': request.form['first_name'].capitalize(),
        'last_name': request.form['last_name'].capitalize(),
        'email': request.form['email']
    }
    Employee.admin_update_employee(this_employee)
    flash('Employee updated successfully', 'employee_updated')
    return redirect('/admin')


@app.route('/admin/assign_product_team/<int:product_id>/<int:invoice_id>', methods=['POST'])
def assign_product_team(product_id, invoice_id):
    """
    This function takes in a product_id and an invoice_id, and then creates a product_team record in the
    database
    
    :param product_id: the id of the product that is being assigned to the team
    :param invoice_id: the invoice id of the invoice that the product is being added to
    :return: the redirect to the admin page.
    """
    print(invoice_id)
    this_employee = {
        'employee_id': request.form['employee_id']
    }
    current_employee = Employee.get_employee_by_id(this_employee)
    product_team = {
        'employee_id': int(request.form['employee_id']),
        'employee_email': current_employee.email,
        'product_id': product_id,
        'invoice_id': invoice_id
    }
    Employee.create_product_team(product_team)
    return redirect('/admin')
    


@app.route('/admin/delete_employee/<int:employee_id>')
def delete_employee(employee_id):
    """
    It takes an employee_id as an argument, creates a dictionary with that employee_id, and then passes
    that dictionary to the delete_employee function in the Employee class
    
    :param employee_id: The id of the employee to be deleted
    :return: the redirect function.
    """
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
        'name': request.form['name'].title(),
        'category': request.form['category'].upper(),
        'price': request.form['price']
    }
    Product.create_product(new_product)
    flash('Product added successfully', 'product_added')
    return redirect('/admin')


@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
def edit_product(product_id):
    """
    It updates a product in the database
    
    :param product_id: The id of the product to be edited
    :return: a redirect to the admin page.
    """
    if not Product.validate_product_form_on_creation(request.form):
        return redirect('/admin')
    this_product = {
        'product_id': product_id,
        'name': request.form['name'].title(),
        'price': request.form['price'],
        'discount': request.form['discount'],
        'category': request.form['category'].upper()
    }
    Product.update_product(this_product)
    flash('Product updated successfully', 'product_updated')
    return redirect('/admin')


@app.route('/admin/delete_product/<int:product_id>')
def delete_product(product_id):
    """
    It deletes a product from the database
    
    :param product_id: The id of the product to be deleted
    :return: the redirect function.
    """
    this_product = {
        'product_id': product_id
    }
    Product.delete_product(this_product)
    return redirect('/admin')