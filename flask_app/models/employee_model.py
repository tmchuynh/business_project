from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Employee:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all_employees(cls):
        query = "SELECT * FROM employees"
        result = connectToMySQL(DATABASE).query_db(query)
        list_of_employees = []
        for row in result:
            list_of_employees.append(Employee(row))
        return list_of_employees
    
    @classmethod
    def get_employee_by_id(cls, data):
        query = "SELECT * FROM employees WHERE id = %(employee_id)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) == 0:
            return None
        return Employee(result[0])
    