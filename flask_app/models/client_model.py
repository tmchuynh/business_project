from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Client:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
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
    def create_client(cls, data):
        query = "INSERT INTO clients (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results)
    
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

    