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
        self.client_email = data['client_email']
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
    def get_client_invoices(cls, data):
        query = "SELECT * FROM invoices LEFT JOIN invoices ON clients.client_id = invoices.client_id WHERE clients.client_id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return None
        list_of_invoices = []
        for result in results:
            list_of_invoices.append(Invoice(result))
        return list_of_invoices
        
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
        
    @classmethod
    def add_product_to_invoice(cls, data):
        query = "INSERT INTO product_invoice (invoices_id, invoices_date_due, invoices_clients_email, product_id) VALUES (%(invoices_id)s, %(invoices_date_due)s, %(invoices_clients_email)s, %(product_id)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results