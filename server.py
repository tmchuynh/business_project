from flask_app import app
from flask_app.controllers import employee
from flask_app.controllers import client
from flask_app.controllers import invoice
from flask_app.controllers import product

if __name__ == "__main__":
    app.run( debug = True)