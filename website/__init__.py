from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    
    # Create the Object of Flask
    app = Flask(__name__)

    # Load the Configuration from the config.py file
    app.config.from_object(Config)

    # Initialize the Application for the use with this Database Setup
    db.init_app(app)

    with app.app_context():

        # Import Views and Auth (Routes)
        from .views import views
        from .auth import auth

        # Register the Blueprints used in Views and Auth
        app.register_blueprint(views, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')

        # Create SQL Tables for our Data Models
        db.create_all()

        # add flask-login implementation
        from .models import User

        login_manager = LoginManager()
        login_manager.login_view = 'auth.sign_in'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            print(User.query.get(int(id)))
            return User.query.get(int(id))

        return app
