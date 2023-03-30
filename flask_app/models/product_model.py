from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

from flask_app.models import product_model

class Product:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.discount = data['discount']
        self.category = data['category']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.products = None
        
    @classmethod
    def get_all_products(cls):
        """
        It returns a list of all the products in the database.
        
        :param cls: This is the class name
        :return: A list of all the products in the database.
        """
        query = "SELECT * FROM products"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_products = []
        for result in results:
            list_of_products.append(cls(result))
        return list_of_products
    
    
    @classmethod
    def get_product_by_id(cls, data):
        """
        It takes in a dictionary of data, and returns a product object if the product exists in the
        database, or None if it doesn't
        
        :param cls: This is the class name
        :param data: a dictionary of the data we want to pass to the database
        :return: A dictionary of the product with the id that was passed in.
        """
        query = "SELECT * FROM products WHERE id = %(product_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    
    @classmethod
    def get_product_by_employee_id(cls, data):
        """
        This function takes in a dictionary of data, and returns a list of Product objects
        
        :param cls: This is the class name
        :param data: a dictionary of the data you want to pass to the query
        :return: A list of products that belong to the employee with the given employee_id.
        """
        query = "SELECT * FROM products WHERE employee_id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        list_of_products = []
        for result in results:
            list_of_products.append(cls(result))
        return list_of_products
    
    
    @classmethod
    def get_product_by_category(cls, data):
        """
        This function takes in a category and returns a list of all the products in that category
        
        :param cls: This is the class name
        :param data: a dictionary of the data you want to pass to the query
        :return: A list of products that are in the category that was passed in.
        """
        query = "SELECT * FROM products WHERE category = %(category)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        list_of_products = []
        for result in results:
            list_of_products.append(cls(result))
        return list_of_products
    

    
    @classmethod
    def create_product(cls, data):
        """
        This function takes in a dictionary of data, and inserts it into the database
        
        :param cls: This is the class that the method is being called on. In this case, it's the Product
        class
        :param data: a dictionary of the data we want to insert into the database
        :return: The id of the product that was just created.
        """
        query = "INSERT INTO products (name, price, category, status) VALUES (%(name)s, %(price)s, %(category)s, 'unassigned')"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def update_product(cls, data):
        """
        This function updates the product with the given data
        
        :param cls: This is the class name
        :param data: a dictionary of the data we want to update in the database
        :return: The results of the query.
        """
        query = "UPDATE products SET price = %(price)s, status = %(status)s, discount = %(discount)s WHERE id = %(product_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def delete_product(cls, data):
        """
        This function deletes a product from the database
        
        :param cls: This is the class name
        :param data: a dictionary of the data you want to insert into the database
        :return: The results of the query.
        """
        query = "DELETE FROM products WHERE id = %(product_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def assign_to_employee(cls, data):
        """
        This function takes in a dictionary of data, and inserts it into the product_team table
        
        :param cls: the class name
        :param data: a dictionary of the data you want to insert into the database
        :return: The results of the query.
        """
        query = "INSERT INTO product_teams (product_id, employee_email, employee_id) VALUES (%(product_id)s, %(employee_email)s, %(employee_id)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    
    @classmethod
    def validate_product_form_on_creation(cls, data):
        """
        If the name is less than 5 characters, flash a message and set is_valid to False. If the category is
        less than 5 characters, flash a message and set is_valid to False. If the price is less than 3,
        flash a message and set is_valid to False
        
        :param cls: The class that the method is being called on
        :param data: This is the data that is passed in from the form
        :return: is_valid
        """
        is_valid = True
        if len(data['name']) < 5:
            flash('Name must be at least 5 characters long', 'product_creation')
            is_valid = False
        if len(data['category']) < 5:
            flash('Category must be at least 5 characters long', 'product_creation')
            is_valid = False
        if float(data['price']) < 3:
            flash('Price must be at least 3', 'product_creation')
            is_valid = False
        return is_valid