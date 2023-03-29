from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


import re

class Billing_Address:
    def __init__(self, data):
        self.id = data['id']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip_code = data['zip_code']
        
        
    @classmethod
    def create_billing_address(cls, data):
        query = "INSERT INTO billing_address (address, city, state, zip_code) VALUES (%(address)s, %(city)s, %(state)s, %(zip_code)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def get_billing_by_address(cls, data):
        query = "SELECT * FROM billing_address WHERE %(address)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return None
        return cls(results[0])