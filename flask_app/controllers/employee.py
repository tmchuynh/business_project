from flask import Flask, render_template, request, redirect, session, flash, session
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
    return redirect('/')


@app.route('/employee')
def employee_login_form():
    return render_template('employee_login.html')


@app.route('/employee/<int:id>')
def employee_update_form(id):
    """
    This function is used to render the employee_update_password.html page.
    
    :param id: the id of the employee to be updated
    :return: The employee_update_password.html page is being returned.
    """
    this_employee = {
        'employee_id': id
    }
    employee = Employee.get_employee_by_id(this_employee)
    return render_template('employee_update_password.html', employee=employee)


@app.route('/employee/update/<int:id>', methods=['POST'])
def employee_update(id):
    """
    This function updates the employee's password
    
    :param id: the id of the employee to update
    """
    if not Employee.validate_employee_form_on_update(request.form):
        return redirect(f'/employee/{id}')
    
    # update employee password
    this_employee = {
        'employee_id': id,
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    
    this_id = {
        'employee_id': id
    }
    
    # employee is done
    current_employee = Employee.get_employee_by_id(this_id)
    print("logged in ", current_employee)
    session['first_name'] = current_employee.first_name
    session['last_name'] = current_employee.last_name
    session['employee_id'] = current_employee.id
    session['email'] = current_employee.email
    
    Employee.update_employee(this_employee)
    # need to redirect to employee login page
    return redirect('/employee')


@app.route('/employee/login', methods=['POST'])
def employee_login():
    """
    If the employee exists, and the password is correct, then the employee is logged in and redirected
    to the appropriate page
    :return: The employee's first name, last name, id, and email are being returned.
    """
    get_email = {
        'email': request.form['email']
    }
    this_employee = Employee.get_employee_by_email(get_email)
    
    if not this_employee:
        flash("Invalid email or password", "login")
        return redirect('/employee')
    
    if not bcrypt.check_password_hash(this_employee.password, request.form['password']):
        flash('Incorrect password', "login")
        return redirect('/employee')

    if this_employee.new_employee == b'0':
        return redirect(f'/employee/{this_employee.id}')
    else:
        # employee has logged in
        session['first_name'] = this_employee.first_name
        session['last_name'] = this_employee.last_name
        session['employee_id'] = this_employee.id
        session['email'] = this_employee.email
        return redirect('/employee/get_clients')


@app.route('/employee/home')
def employee_home():
    return render_template('employee_home.html')