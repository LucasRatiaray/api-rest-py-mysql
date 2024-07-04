from flask import Flask
from flask_mysqldb import MySQL
from .config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    with app.app_context():
        from .routes import register_routes
        register_routes(app)

    return app
