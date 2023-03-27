from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.payment_method_model import Payment_Method
