from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import employee_model

import re

class Client:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.employee = None
        
        
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
        query = "SELECT * FROM clients WHERE id = %s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
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
    def create_relationship_with_employee(cls, data):
        """
        This function creates a relationship between a client and an employee
        
        :param cls: the class name
        :param data: a dictionary of the data we want to pass to the query
        :return: The results of the query.
        """
        query = "INSERT INTO client_employee_relationship (clients_id, clients_email, employee_id, employee_email) VALUES (%(client_id)s, %(client_email)s, %(employee_id)s, %(employee_email)s)"
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
        query = """SELECT clients.*, employee.first_name, employee.last_name, employee.email FROM clients
        LEFT JOIN client_employee_relationship ON client_employee_relationship.clients_id = clients.id
        LEFT JOIN employee ON client_employee_relationship.employee_id = employee.id
        WHERE employee.id = %(employee_id)s"""
        
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        if len(results):
            client = cls(results[0])
            client.employee = []
            
            for result in results:
                if not result['employee_id']:
                    break
                
                employee = {
                    'id': result['id'],
                    'first_name': result['first_name'],
                    'last_name': result['last_name'],
                    'email': result['email'],
                    'created_at': result['created_at'],
                    'updated_at': result['updated_at']
                }
                client.employee.append(employee_model.Employee(employee))
            return client
        return None

    
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
        query = "SELECT * FROM clients WHERE  email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return True
        return False
        
        
    @staticmethod
    def validate_client(data):
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