from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import employee_model

import re

class Client:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.employee = None
        
        
    @classmethod
    def get_all_clients(cls):
        query = "SELECT * FROM clients"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_clients = []
        for result in results:
            list_of_clients.append(cls(result))
        return list_of_clients
    
    
    @classmethod
    def get_client_by_id(cls, data):
        query = "SELECT * FROM clients WHERE id = %s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return None
        return cls(results[0])
    
    
    @classmethod
    def get_client_by_employee(cls, data):
        query = """SELECT * FROM clients
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
        query = "INSERT INTO clients (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def update_client(cls, data):
        query = "UPDATE clients SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results)
    
    
    @classmethod
    def delete_client(cls, data):
        query = "DELETE FROM clients WHERE id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results)

    
    @classmethod
    def check_database(cls, data):
        query = "SELECT * FROM clients WHERE  email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return True
        return False
        
        
    @staticmethod
    def validate_client(data):
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