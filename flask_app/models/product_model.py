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
        self.employee_id = data['employee_id']
        self.employee_id = data['employee_id']
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