from flask import Flask, render_template, request, redirect
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.employee_model import Employee

@app.route('/')
def index():
    return render_template('index.html')