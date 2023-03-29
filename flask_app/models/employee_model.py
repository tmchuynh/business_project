from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import client_model

import re

class Employee:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.temp_password = data['temp_password']
        self.new_employee = data['new_employee']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.clients = None
        
        
    @classmethod
    def get_all_employees(cls):
        """
        It returns a list of all the employees in the database.
        
        :param cls: This is the class name
        :return: A list of all the employees in the database.
        """
        query = "SELECT * FROM employees"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_employees = []
        if not results:
            return list_of_employees
        for result in results:
            list_of_employees.append(cls(result))
        return list_of_employees
    
    
    @classmethod
    def get_employee_by_id(cls, data):
        """
        It takes in a dictionary of data, and returns an Employee object if the employee exists, or None if
        the employee does not exist
        
        :param cls: This is the class that the method is being called on. In this case, it's the Employee
        class
        :param data: a dictionary of the data we want to pass to the query
        :return: A dictionary of the employee's information.
        """
        query = "SELECT * FROM employees WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return None
        return Employee(results[0])
    
    
    @classmethod
    def get_employee_by_email(cls, data):
        """
        It takes in a dictionary of data, and returns an Employee object if the employee exists, or None if
        the employee does not exist
        
        :param cls: This is the class that the method is being called on. In this case, it's the Employee
        class
        :param data: a dictionary of the data we want to pass to the query
        :return: A dictionary of the employee's information.
        """
        query = "SELECT * FROM employees WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return None
        return Employee(results[0])
    
    
    @classmethod
    def create_employee(cls, data):
        """
        The function takes in a dictionary of data, and then uses that data to create a new employee in the
        database
        
        :param cls: This is the class that the method is being called on. In this case, it's the Employee
        class
        :param data: a dictionary of the data we want to insert into the database
        :return: The id of the employee that was just created.
        """
        query = "INSERT INTO employees (first_name, last_name, email, password, temp_password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(temp_password)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def get_client_by_employee(cls, data):
        """
        > This function returns a client object with a list of employee objects that are associated with the
        client
        
        :param cls: The class that is calling the method
        :param data: a dictionary of the data we want to pass to the query
        :return: A client object with a list of employees
        """
        query = """SELECT clients.*, employees.* FROM employees
        LEFT JOIN client_employee_relationships ON client_employee_relationships.employee_id = employees.id
        LEFT JOIN clients ON client_employee_relationships.clients_email = clients.email
        WHERE employees.id = %(employee_id)s"""
        
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if results:
            employee = cls(results[0])
            employee.clients = []
            
            for result in results:
                # print(result)
                if not result['id']:
                    break
                
                client = {
                    'id': result['id'],
                    'first_name': result['first_name'],
                    'last_name': result['last_name'],
                    'email': result['email'],
                    'password': result['password'],
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at']
                }
                employee.clients.append(client_model.Client(client))
                print(employee)
            return employee
        return []
    
    
    @classmethod
    def update_employee(cls, data):
        """
        This function updates the employee's first name, last name, and email address in the database
        
        :param cls: This is the class name
        :param data: a dictionary of the data we want to update in the database
        :return: The results of the query.
        """
        query = "UPDATE employees SET new_employee = b'1', password = %(password)s, temp_password = 'employee updated' WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def admin_update_employee(cls, data):
        """
        This function updates the employee's first name, last name, and email address in the database
        
        :param cls: This is the class that the method is being called on. In this case, it's the User class
        :param data: a dictionary of the data we want to update in the database
        :return: The results of the query.
        """
        query = "UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def delete_employee(cls, data):
        """
        This function deletes an employee from the database
        
        :param cls: This is the class that the method is being called on. In this case, it's the Employee
        class
        :param data: a dictionary of the data you want to insert into the database
        :return: The results of the query.
        """
        query = "DELETE FROM employees WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def create_client_employee_relationship(cls, data):
        """
        This function creates a relationship between a client and an employee
        
        :param cls: This is the class that the method is being called on
        :param data: a dictionary of the data you want to insert into the database
        :return: The results of the query.
        """
        query = "INSERT INTO client_relationships (client_email, employee_email) VALUES (%(client_email)s, %(employee_email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def create_product_team(cls, data):
        """
        This function creates a new product team by inserting a new row into the product_teams table
        
        :param cls: the class that this method belongs to
        :param data: {}
        :return: The results of the query.
        """
        query = "INSERT INTO product_teams (employee_id, employee_email, product_id, invoice_id) VALUES(%(employee_id)s, %(employee_email)s, %(product_id)s, %(invoice_id)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        return results

    
    
    @classmethod
    def check_database(cls, data):
        """
        The function takes in a dictionary of data, and returns True if the email is in the database, and
        False if it is not
        
        :param cls: This is the class that the method is being called on
        :param data: a dictionary of the data we want to insert into the database
        :return: The query is being returned.
        """
        query = "SELECT * FROM employees WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return False
        return True
    

    @staticmethod
    def validate_employee_form_on_creation(data):
        """
        This function checks to see if the first name, last name, and email are valid. If they are not, it
        will flash a message to the user
        
        :param data: a dictionary of the form data
        :return: A boolean value
        """
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        if (regex.search(data['first_name']) != None or len(data['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not meet minimum length requirements.', "registration")
            is_valid = False
        
        if (regex.search(data['last_name'])!= None or len(data['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not meet minimum length requirements.', "registration")
            is_valid = False
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if len(data['email']) == 0:
            flash('Email cannot be empty.', "registration")
            is_valid = False
        else:    
            if (re.fullmatch(regex, data['email'])):
                # email is valid
                # need to check if the email is already in use
                this_user = {
                    'email': data['email']
                }
                results = Employee.check_database(this_user)
                
                if results:
                    flash('Email is already in use, please use a different email', "registration")
                    is_valid = False
            else:
                flash('Email contains special characters', "registration")
                is_valid = False
        
        return is_valid
    
    
    @staticmethod
    def validate_employee_form_on_admin_update(data):
        """
        This function checks to see if the first name, last name, and email are valid. If they are not, it
        will flash a message to the user
        
        :param data: a dictionary of the form data
        :return: A boolean value
        """
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        if (regex.search(data['first_name']) != None or len(data['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not meet minimum length requirements.', "admin_update_employee")
            is_valid = False
        
        if (regex.search(data['last_name'])!= None or len(data['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not meet minimum length requirements.', "admin_update_employee")
            is_valid = False
        
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if len(data['email']) == 0:
            flash('Email cannot be empty.', "admin_update_employee")
            is_valid = False
        else:    
            if (re.fullmatch(regex, data['email'])):
                # email is valid
                # need to check if the email is already in use
                this_user = {
                    'email': data['email']
                }
                results = Employee.check_database(this_user)
                
                if results:
                    flash('Email is already in use, please use a different email', "admin_update_employee")
                    is_valid = False
            else:
                flash('Email contains special characters', "admin_update_employee")
                is_valid = False
        
        return is_valid
    
    
    @staticmethod
    def validate_employee_form_on_update(data):
        """
        The function validates the employee form on update
        
        :param data: the data that was submitted in the form
        :return: is_valid
        """
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        if (len(data['password']) < 8):
            # password is too short
            flash('Password is too short', "registration")
            is_valid = False
            
        if (re.search('[0-9]', data['password']) == None):
            # password does not contain digits
            flash('Password does not contain digits', "registration")
            is_valid = False
            
        if (re.search('[A-Z]', data['password']) == None):
            # password does not contain uppercase letters
            flash('Password does not contain a uppercase letters', "registration")
            is_valid = False
            
        if (regex.search(data['password']) == None):
            # password contains not special characters
            flash('Password contains not a special characters', "registration")
            is_valid = False
        
        if (data['password']!= data['password_confirmation']):
            flash('Passwords do not match', "registration")
            is_valid = False
        
        return is_valid
        