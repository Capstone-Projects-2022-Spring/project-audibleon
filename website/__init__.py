from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    
    # Create the Object of Flask
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 'as;dlfkja;sdlkjf'

    # Load the Configuration from the config.py file
    app.config.from_object(Config)

    # Initialize the Application for the use with this Database Setup
    db.init_app(app)

    with app.app_content():

        # Import Views and Auth (Routes)
        from .views import views
        from .auth import auth

        # Register the Blueprints used in Views and Auth
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        # Create SQL Tables for our Data Models
        db.create_all()

        return app