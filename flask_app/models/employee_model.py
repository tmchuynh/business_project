from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

import re

class Employee:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.new_employee = data['new_employee']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_employees(cls):
        """
        It returns a list of all the employees in the database.
        
        :param cls: This is the class name
        :return: A list of all the employees in the database.
        """
        query = "SELECT * FROM employee"
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
        query = "SELECT * FROM employee WHERE id = %(employee_id)s"
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
        query = "SELECT * FROM employee WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
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
        query = "INSERT INTO employee (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def update_employee(cls, data):
        """
        This function updates the employee's first name, last name, and email address in the database
        
        :param cls: This is the class name
        :param data: a dictionary of the data we want to update in the database
        :return: The results of the query.
        """
        query = "UPDATE employee SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, new_employee = 1, password = %(password)s WHERE id = %(employee_id)s"
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
        query = "DELETE FROM employee WHERE id = %(employee_id)s"
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
        query = "INSERT INTO client_relationship (client_email, employee_email) VALUES (%(client_email)s, %(employee_email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
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
        query = "SELECT * FROM employee WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return False
        return True
    

    @staticmethod
    def validate_employee_form(data):
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
        