from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Employee:
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_employees(cls):
        query = "SELECT * FROM employees"
        results = connectToMySQL(DATABASE).query_db(query)
        list_of_employees = []
        for result in results:
            list_of_employees.append(cls(result))
        return list_of_employees
    
    @classmethod
    def get_employee_by_id(cls, data):
        query = "SELECT * FROM employees WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) == 0:
            return None
        return Employee(results[0])
    
    @classmethod
    def create_employee(cls, data):
        query = "INSERT INTO employees (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def update_employee(cls, data):
        query = "UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def delete_employee(cls, data):
        query = "DELETE FROM employees WHERE id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    