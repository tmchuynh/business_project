from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.employee_model import Employee
import random, string

@app.route('/admin')
def admin():
    list_of_employees = Employee.get_all_employees()
    return render_template('admin.html', list_of_employees=list_of_employees)

@app.route('/admin/add_employee', methods=['POST'])
def add_employee():
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
    return redirect('/admin')