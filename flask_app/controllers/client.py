from flask import Flask, render_template, request, redirect, flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.client_model import Client
from flask_app.models.employee_model import Employee
from flask_app.models.product_model import Product

@app.route('/clients')
def display_product():
    """
    It gets all the products from the database, and then renders a template that displays them
    :return: A list of all the products in the database.
    """
    if 'buying' not in session:
        session['buying'] = []
    list_of_products = Product.get_all_products()
    return render_template('display_all_products.html', list_of_products=list_of_products)


@app.route('/clients/options/<int:product_id>')
def show_client_options(product_id):
    """
    If the user is logged in, show them the cart page. If they're not logged in, show them the create
    client page.
    :return: the render_template function.
    """
    if 'client_email' not in session:
        return render_template('client_login_reg.html')
    
    # It's checking to see if the product_id is in the session['buying'] list. If it's not, it adds it to
    # the list.
    if product_id not in session['buying']:
        session['buying'] += [product_id]
    print(f"session has {len(session['buying'])} items in it")
    return redirect('/clients/cart')


@app.route('/clients/cart')
def show_cart():
    """
    It gets the list of products from the session, gets the product details from the database,
    calculates the total price, and then renders the cart.html template
    :return: A list of products and the total price of the products in the cart.
    """
    list_of_products = []
    total_price = 0
    for item in session['buying']:
        this_item = {
            'product_id': item,
        }
        this_product = Product.get_product_by_id(this_item)
        
        # It's calculating the price of the product after the discount has been applied.
        total_price += (this_product.price - (this_product.price * this_product.discount))
        
        list_of_products.append(this_product)
    return render_template('cart.html', list_of_products=list_of_products, total_price=total_price)


@app.route('/clients/login', methods=['POST'])
def check_for_client_in_database():
    """
    If the client's login information is not valid, redirect them to the client options page. Otherwise,
    set the client's email in the session and redirect them to the client's page
    :return: a redirect to the clients page.
    """
    if not Client.validate_client_login(request.form):
        return redirect('/clients/register_form')
    if request.form['password'] == 'password123456':
        this_client = {
            'email': request.form['email']
        }
        client = Client.get_client_by_email(this_client)
        session['client_id'] = client.id
        return redirect(f'/clients/update_password_form/{client.id}')
    session['client_first_name'] = request.form['first_name']
    session['client_email'] = request.form['email']

    return redirect('/clients')


@app.route('/clients/update_password_form/<int:id>')
def update_password_form(id):
    this_client = {
        'client_id': id
    }
    client = Client.get_client_by_id(this_client)
    print("new password", client.password)
    return render_template("client_update_password.html", client=client)


@app.route('/client/update/<int:id>', methods=['POST'])
def update_password(id):
    if not Client.validate_client_password_update(request.form):
        return redirect(f'/clients/update_password_form/{id}')
    
    this_client = {
        'client_id': id,
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    
    this_id = {
        'client_id': id
    }
    
    current_client = Client.get_client_by_id(this_id)
    print("logged in client ", current_client)
    session['client_first_name'] = current_client.first_name
    session['client_email'] = current_client.email
    session['client_id'] = current_client.id
    
    Client.change_client_passwords(this_client)
    return redirect('/clients')
    


@app.route('/clients/register_form')
def client_reg_form():
    return render_template("client_login_reg.html")


@app.route('/clients/register', methods=['GET', 'POST'])
def register_client():
    """
    If the user is not logged in, validate the form data, create a new client, and redirect to the cart
    page
    :return: the cart.html template.
    """
    if 'client_email' not in session:
        if not Client.client_reg_validate_client(request.form):
            return redirect('/clients/register_form')
        
        # create a new client
        new_client = {
            'first_name': request.form['first_name'].capitalize(),
            'last_name': request.form['last_name'].capitalize(),
            'email': request.form['email'],
            'password': request.form['password'],
        }
        Client.create_client(new_client)
        c = Client.get_client_by_email(new_client)
        print("new client is ", Client.get_client_by_email(new_client))
        flash('You have successfully registered!', 'client_success')
        
        # store the new client in the session
        session['client_first_name'] = request.form['first_name'].capitalize()
        session['client_email'] = new_client['email']
        session['client_id'] = new_client['id']
        print("logged in client ", session['client_email'])
        
        # create the relationship between the client and the employee
        # employee information
        this_employee = {
            'email': request.form['employee_email']
        }
        e = Employee.get_employee_by_email(this_employee)
        print(e)
        relationship = {
            'client_id': c.id,
            'client_email': session['client_email'],
            'employee_id': e.id,
            'employee_email': request.form['employee_email']
        }
        Client.create_relationship_with_employee(relationship)
        
        
        return redirect('/clients')
    session['buying'] = []
    return render_template('cart.html')


@app.route('/employee/add_client', methods=['POST'])
def add_client():
    """
    The function creates a new client and then creates a relationship between the new client and the
    employee who created the client
    :return: The redirect is returning the employee's home page.
    """
    if not Client.employee_validate_client(request.form):
        return redirect('/employee/get_clients')
    
    # when employee manually enters in a client, the temp password will be 'password123456'
    new_client = {
        'first_name': request.form['first_name'].capitalize(),
        'last_name': request.form['last_name'].capitalize(),
        'email': request.form['email'],
        'employee_email': session['email'],
        'password': bcrypt.generate_password_hash('password123456')
    }
    Client.create_client(new_client)
    flash('Client added successfully', 'client_added')
    current_client = Client.get_client_by_email(new_client)
    print("new client added ", current_client)
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