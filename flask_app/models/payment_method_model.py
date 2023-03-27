from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

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
        query = "IINSERT INTO payment_method (card_number, expiration_date, CVC, clients_id, clients_email) VALUES (%(card_number)s, %(expiration_date)s, %(CVC)s, %(clients_id)s, %(clients_email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results