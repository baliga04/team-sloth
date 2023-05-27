from flask import Flask
from config import Config

from app.extensions import db,bcrypt

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config) # Loading the config file

    # Initializing Flask extensions here

    # Flask SQLAlchemy
    db.init_app(app)

    # Creating the database tables (if not present)

    from app.models.user import User
    from app.models.budgets import Budgets
    from app.models.transactions import Transactions
    
    with app.app_context():
        db.create_all()

    # Bcrypt
    bcrypt.init_app(app)
    


    # Registering the blueprints here
    # from app.refugee_endpoints import bp as refugee_bp
    # app.register_blueprint(refugee_bp)

    
    # @app.route('/test/')
    # def test_page():
    #     return '<h1>Testing</h1>'

    return app