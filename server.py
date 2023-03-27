from flask_app import app
from flask_app.controllers import employee
from flask_app.controllers import client
from flask_app.controllers import invoice
from flask_app.controllers import product
from flask_app.controllers import admin
from flask_app.controllers import payment_method

if __name__ == "__main__":
    app.run( debug = True)