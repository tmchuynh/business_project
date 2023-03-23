from flask import Flask, render_template, request, redirect, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.employee_model import Employee

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

@app.route('/employee')
def employee_login_form():
    return render_template('employee_login.html')


@app.route('/employee/login', methods=['POST'])
def employee_login():
    get_email = {
        'email': request.form['email']
    }
    this_user = Employee.get_employee_by_email(get_email)
    
    if not this_user:
        flash("Invalid email or password", "login")
        return redirect('/employee')
    
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash('Incorrect password', "login")
        return redirect('/employee')
    
    print(this_user.new_employee)

    if this_user.new_employee == b'0':
        return redirect(f'/employee/{this_user.id}')
    else:
        return redirect('/employee/home')

@app.route('/employee/<int:id>')
def employee_update_form(id):
    this_employee = {
        'employee_id': id
    }
    employee = Employee.get_employee_by_id(this_employee)
    return render_template('employee_update_password.html', employee=employee)

@app.route('/employee/update/<int:id>', methods=['POST'])
def employee_update(id):
    if not Employee.validate_employee_form(request.form):
        return redirect(f'/employee/update/{id}')
    this_employee = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    Employee.update_employee(this_employee)
    return redirect('/employee/home')