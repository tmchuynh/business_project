from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Invoice:
    def __init__(self, data):
        self.id = data['id']
        self.amount = data['amount']
        self.fee = data['fee']
        self.date_due = data['date_due']
        self.date_paid = data['date_paid']
        self.client_email = data['client_email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_invoice_by_client_id(cls, data):
        """
        It returns the invoice for a given client_id.
        
        :param cls: This is the class name
        :param data: a dictionary of the data you want to pass to the query
        :return: A list of dictionaries.
        """
        query = "SELECT * FROM invoices WHERE client_id = %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def get_invoice_by_date_due(cls, data):
        """
        This function takes in a date_due and returns an Invoice object if the date_due exists in the
        database
        
        :param cls: the class name
        :param data: a dictionary of the data you want to pass to the query
        :return: A list of dictionaries.
        """
        query = "SELECT * FROM invoices WHERE date_due = %(date_due)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def get_client_invoices(cls, data):
        """
        This function takes in a client_id and returns a list of Invoice objects that belong to that client
        
        :param cls: the class that the method is being called on
        :param data: a dictionary of the data you want to pass to the query
        :return: A list of Invoice objects
        """
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
        """
        This function creates a new invoice in the database and returns an Invoice object
        
        :param cls: the class name
        :param data: a dictionary of the data to be inserted into the database
        :return: The results of the query.
        """
        query = "INSERT INTO invoices (amount, tax, date_due, date_paid, client_id) VALUES (%(amount)s, %(tax)s, %(date_due)s, %(date_paid)s, %(client_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def update_invoice(cls, data):
        """
        This function updates the invoice in the database with the given data
        
        :param cls: the class name
        :param data: a dictionary of the data to be updated
        :return: The results of the query.
        """
        query = "UPDATE invoices SET amount = %(amount)s, tax = %(tax)s, date_due = %(date_due)s, date_paid = %(date_paid)s, WHERE id = %(invoice_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
    
    @classmethod
    def delete_invoice(cls, data):
        """
        This function deletes an invoice from the database
        
        :param cls: the class name
        :param data: a dictionary of the data you want to insert into the database
        :return: The results of the query.
        """
        query = "DELETE FROM invoices WHERE id = %(invoice_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) > 0:
            return Invoice(results[0])
        else:
            return None
        
    @classmethod
    def add_product_to_invoice(cls, data):
        """
        This function takes in a dictionary of data, and inserts it into the product_invoice table
        
        :param cls: the class name
        :param data: {
        :return: The results of the query.
        """
        query = "INSERT INTO product_invoices (invoices_id, invoices_date_due, invoices_clients_email, product_id) VALUES (%(invoices_id)s, %(invoices_date_due)s, %(invoices_clients_email)s, %(product_id)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results