from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models import product_model
from flask_app.models import employee_model

import re

class Client:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.payment_id = data['payment_id']
        self.products = None
        
        
    @classmethod
    def get_all_clients(cls):
        """
        It returns a list of all the clients in the database.
        
        :param cls: This is the class name
        :return: A list of all the clients in the database.
        """
        query = "SELECT * FROM clients"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_clients = []
        for result in results:
            list_of_clients.append(cls(result))
        return list_of_clients
    
    
    @classmethod
    def get_client_by_id(cls, data):
        """
        `get_client_by_id` takes in a client's id and returns a client object
        
        :param cls: the class that the method belongs to
        :param data: This is the data that we're passing into the query
        :return: A dictionary of the client's information.
        """
        query = "SELECT * FROM clients WHERE id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    
    
    @classmethod
    def get_client_by_email(cls, data):
        """
        This function takes in a dictionary of data, and returns a client object if the email exists in the
        database
        
        :param cls: This is the class that the method is being called on. In this case, it's the User class
        :param data: a dictionary of the data we want to insert into the database
        :return: A dictionary of the user's information.
        """
        query = "SELECT * FROM clients WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    
    
    @classmethod
    def get_product_by_client(cls, data):
        """
        It gets all the products that a client has purchased.
        
        :param cls: This is the class that we are calling the method on. In this case, it's the Client class
        :param data: This is the data that we're passing into the query
        :return: A list of dictionaries
        """
        query = """SELECT * FROM product_invoices
        INNER JOIN invoices ON product_invoices.clients_email = invoices.clients_email
        INNER JOIN clients ON invoices.clients_email = clients.email
        WHERE clients.id = %(client_id)s"""
        
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            client = cls(results[0])
            client.products = []
            
            for result in results:
                
                if not result['email']:
                    break
                
                product = {
                    'id': result['id'],
                    'name': result['name'],
                    'category': result['category'],
                    'discount': result['discount'],
                    'price': result['price'],
                    'status': result['status'],
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at']
                }
                client.products.append(product_model.Product(product))
                print(product)
            return client
        return []
            
    
    @classmethod
    def create_relationship_with_employee(cls, data):
        """
        This function creates a relationship between a client and an employee
        
        :param cls: the class name
        :param data: a dictionary of the data we want to pass to the query
        :return: The results of the query.
        """
        query = "INSERT INTO client_employee_relationships (clients_id, clients_email, employee_id, employee_email) VALUES (%(client_id)s, %(client_email)s, %(employee_id)s, %(employee_email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    
    @classmethod
    def create_client(cls, data):
        """
        The function takes in a dictionary of data, and then uses that data to create a new row in the
        database
        
        :param cls: This is the class that the method is being called on. In this case, it's the Client
        class
        :param data: a dictionary of the data we want to insert into the database
        :return: The id of the client that was just created.
        """
        query = "INSERT INTO clients (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def update_client(cls, data):
        """
        This function updates the client's first name, last name, and email in the database
        
        :param cls: This is the class name
        :param data: a dictionary of the data we want to update in the database
        :return: The results of the query.
        """
        query = "UPDATE clients SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results)
    
    
    @classmethod
    def change_client_passwords(cls, data):
        """
        This function takes in a dictionary of data, and updates the password of the client with the email
        that matches the email in the dictionary
        
        :param cls: the class name
        :param data: a dictionary of the data we want to insert into the database
        :return: The results of the query.
        """
        query = "UPDATE clients SET password = %(password)s WHERE id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def delete_client(cls, data):
        """
        This function deletes a client from the database
        
        :param cls: the class object that is calling this method
        :param data: a dictionary of the data you want to insert into the database
        :return: The results of the query.
        """
        query = "DELETE FROM clients WHERE id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results)

    
    @classmethod
    def check_database(cls, data):
        """
        The function takes in a dictionary of data, and checks to see if the email is already in the
        database. If it is, it returns True, otherwise it returns False
        
        :param cls: This is the class that the method is being called on
        :param data: a dictionary of the data we want to insert into the database
        :return: True or False
        """
        query = "SELECT * FROM clients WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return True
        return False
        
        
    @staticmethod
    def employee_validate_client(data):
        """
        This function checks to see if the data entered by the user is valid. If it is, it returns True,
        otherwise it returns False
        
        :param data: This is the data that is being passed in from the form
        :return: A boolean value
        """
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        if (regex.search(data['first_name']) != None or len(data['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not meet minimum length requirements.', "new_client")
            is_valid = False
        
        if (regex.search(data['last_name'])!= None or len(data['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not meet minimum length requirements.', "new_client")
            is_valid = False
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if len(data['email']) == 0:
            flash('Email address cannot be empty.', "new_client")
            is_valid = False
        else:
            if (re.fullmatch(regex, data['email'])):
                if not data['email'] == data['email_confirmation']:
                    flash('Emails do not match', "new_client")
                    is_valid = False
                # email is valid
                # need to check if the email is already in use
                this_user = {
                    'email': data['email']
                }
                results = Client.check_database(this_user)
                
                if results:
                    flash('Email is already in use, please use a different email', "new_client")
                    is_valid = False
            else:
                flash('Email contains special characters', "new_client")
                is_valid = False

        
        return is_valid
    
    
    @staticmethod
    def client_reg_validate_client(data):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        if (regex.search(data['first_name']) != None or len(data['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not meet minimum length requirements.', "new_client")
            is_valid = False
        
        if (regex.search(data['last_name'])!= None or len(data['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not meet minimum length requirements.', "new_client")
            is_valid = False
            
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', "new_client")
            is_valid = False
        else:
            if (regex.search(data['password']) == None):
                flash('Password must contain at least one special character', "new_client")
                is_valid = False
            if (re.search('[0-9]', data['password']) == None):
                # password does not contain digits
                flash('Password does not contain at least one number', "new_client")
                is_valid = False
            if (re.search('[A-Z]', data['password']) == None):
                # password does not contain uppercase letters
                flash('Password does not contain at least one uppercase letter', "new_client")
                is_valid = False
            if (data['password']!= data['password_confirmation']):
                flash('Passwords do not match, please try again', "new_client")
                is_valid = False
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if len(data['email']) == 0:
            flash('Email address cannot be empty.', "new_client")
            is_valid = False
        else:
            if (re.fullmatch(regex, data['email'])):
                if not data['email'] == data['email_confirmation']:
                    flash('Emails do not match', "new_client")
                    is_valid = False
                # email is valid
                # need to check if the email is already in use
                this_user = {
                    'email': data['email']
                }
                results = Client.check_database(this_user)
                
                if results:
                    flash('Email is already in use, please use a different email', "new_client")
                    is_valid = False
            else:
                flash('Email contains special characters', "new_client")
                is_valid = False
                        
        if len(data['employee_email']) == 0:
            flash('Employee email address cannot be empty.', "new_client")
            is_valid = False
        else:
            if (re.fullmatch(regex, data['employee_email'])):
                this_employee = {
                    'email': data['employee_email']
                }
                results = employee_model.Employee.check_database(this_employee)
                
                if not results:
                    flash('Cannot find employee in our system, please try again', "new_client")
                    is_valid = False
            else:
                flash('Employee email contains special characters', "new_client")
                is_valid = False
                

        return is_valid
    
    
    @staticmethod
    def validate_client_login(data):
        """
        This function checks to see if the email is in the database, and if the first name is not empty
        
        :param data: This is the data that is being passed in from the form
        :return: A boolean value
        """
        is_valid = True
        this_user = {
            'email': data['email']
        }
        if len(data['email']) == 0:
            flash('Please enter your email address', "check_client_login")
            is_valid = False
        else:
            if not Client.check_database(this_user):
                is_valid = False
                flash('Email is not in use, please use a different email', "check_client_login")
        if len(data['password']) < 1:
            flash('Be sure to enter a password', "check_client_login")
            is_valid = False
        else:
            check = Client.get_client_by_email(this_user)
            print(check)
            
            if not bcrypt.check_password_hash(check.password, data['password']):
                print("Password hash false", data['password'])
                flash('Password is incorrect', "check_client_login")
                is_valid = False
        return is_valid
    
    
    @staticmethod
    def validate_client_password_update(data):
        """
        The function takes in a dictionary of data, and checks to see if the password is at least 8
        characters, contains at least one special character, one number, and one uppercase letter, and if
        the password and password confirmation match. If any of these conditions are not met, the function
        returns False, and if all conditions are met, the function returns True
        
        :param data: the data that is being validated
        :return: is_valid
        """
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        is_valid = True
        print(data['password'])
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', "new_client")
            is_valid = False
        else:
            if (regex.search(data['password']) == None):
                flash('Password must contain at least one special character', "new_client")
                is_valid = False
            if (re.search('[0-9]', data['password']) == None):
                # password does not contain digits
                flash('Password does not contain at least one number', "new_client")
                is_valid = False
            if (re.search('[A-Z]', data['password']) == None):
                # password does not contain uppercase letters
                flash('Password does not contain at least one uppercase letter', "new_client")
                is_valid = False
            if (data['password']!= data['password_confirmation']):
                flash('Passwords do not match, please try again', "new_client")
                is_valid = False
        return is_valid
            