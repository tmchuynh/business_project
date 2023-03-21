from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Product:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.discount = data['discount']
        self.status = data['status']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_products(cls):
        query = "SELECT * FROM products"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_products = []
        for result in results:
            list_of_products.append(cls(result))
        return list_of_products
    
    @classmethod
    def get_product_by_employee_id(cls, data):
        query = "SELECT * FROM products WHERE employee_id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        list_of_products = []
        for result in results:
            list_of_products.append(cls(result))
        return list_of_products
    
    @classmethod
    def get_product_by_category(cls, data):
        query = "SELECT * FROM products WHERE category = %(category)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        list_of_products = []
        for result in results:
            list_of_products.append(cls(result))
        return list_of_products
    
    @classmethod
    def create_product(cls, data):
        query = "INSERT INTO products (name, price, discount, status, category, employee_id) VALUES (%(name)s, %(price)s, %(discount)s, %(status)s, %(category)s, %(employee_id)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def update_product(cls, data):
        query = "UPDATE products SET name = %(name)s, price = %(price)s, discount = %(discount)s, status = %(status)s, category = %(category)s, employee_id = %(employee_id)s WHERE id = %(product_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE id = %(product_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def assign_to_employee(cls, data):
        query = "INSERT INTO product_team (product_id, employee_email) VALUES (%(product_id)s, %(employee_email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results