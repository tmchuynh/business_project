from flask import Flask, render_template, request, redirect, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.employee_model import Employee
from flask_app.models.product_model import Product
import random, string

@app.route('/admin')
def admin():
    """
    It gets all the employees from the database and passes them to the admin.html template
    :return: A list of all employees
    """
    list_of_employees = Employee.get_all_employees()
    list_of_products = Product.get_all_products()
    return render_template('admin.html', list_of_employees=list_of_employees, list_of_products=list_of_products)

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


@app.route('/admin/add_product', methods=['POST'])
def add_product():
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