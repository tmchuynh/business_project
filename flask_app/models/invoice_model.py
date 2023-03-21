from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Invoice:
    def __init__(self, data):
        self.id = data['id']
        self.amount = data['amount']
        self.fee = data['fee']
        self.tax = data['tax']
        self.date_due = data['date_due']
        self.date_paid = data['date_paid']
        self.status = data['status']
        self.client_id = data['client_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_invoice_by_client_id(cls, data):
        query = "SELECT * FROM invoices WHERE client_id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def get_invoice_by_date_due(cls, data):
        query = "SELECT * FROM invoices WHERE date_due = %(date_due)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def create_invoice(cls, data):
        query = "INSERT INTO invoices (amount, fee, tax, date_due, date_paid, status, client_id) VALUES (%(amount)s, %(fee)s, %(tax)s, %(date_due)s, %(date_paid)s, %(status)s, %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def update_invoice(cls, data):
        query = "UPDATE invoices SET amount = %(amount)s, fee = %(fee)s, tax = %(tax)s, date_due = %(date_due)s, date_paid = %(date_paid)s, status = %(status)s WHERE id = %(invoice_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
    
    @classmethod
    def delete_invoice(cls, data):
        query = "DELETE FROM invoices WHERE id = %(invoice_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None