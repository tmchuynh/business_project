from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from datetime import date

import re

class Payment_Method:
    def __init__(self, data):
        self.id = data['id']
        self.card_number = data['card_number']
        self.expiration_date = data['expiration_date']
        self.CVC = data['CVC']
        self.clients_id = data['clients_id']
        self.clients_email = data['clients_email']
        
    @classmethod
    def create_payment_method(cls, data):
        """
        This function takes in a dictionary of data and inserts it into the database
        
        :param cls: the class name
        :param data: a dictionary of the data we want to insert into the database
        :return: The results of the query.
        """
        # need to fix the query to insert payment method
        query = "INSERT INTO payment_methods (card_number, expiration_date, CVC, clients_id, clients_email) VALUES (%(card_number)s, %(expiration_date)s, %(CVC)s, %(clients_id)s, %(clients_email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @staticmethod
    def validate_payment_method(data):
        """
        It checks if the credit card number is valid, and if the CVC is a number
        
        :param data: the data that was submitted in the form
        :return: A boolean value
        """
        is_valid = True
        
        pattern = '^[973][0-9]{16}|[973][0-9]{3}-[0-9]{4}-[0-9]{4}-[0-9]{4}$'
        
        # card_number:
        # must contain exactly 16 digits
        # should only contain 0-9 digits
        # must start with either 9 or 7 or 3
        if (re.match(pattern, data['card_number'])):
            flash("Credit card number is invalid", "payment_validation")
            is_valid = False
            
        if not data['expiration_date'] > date.today():
            is_valid = False
            flash("Expiration date is invalid", "payment_validation")
            
        if not data['CVC'].isdigit():
            flash("Invalid CVC", "payment_validation")
            is_valid = False
            if len(data['CVC']) != 3:
                flash("Invalid CVC length", "payment_validation")
                is_valid = False
                
            
        return is_valid