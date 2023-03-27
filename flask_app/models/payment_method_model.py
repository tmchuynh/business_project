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