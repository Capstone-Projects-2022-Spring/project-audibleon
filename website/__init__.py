from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

# Next Two Lines are to Ensure there are not too many Packets in Payload
from engineio.payload import Payload
Payload.max_decode_packets = 16

# Initialize the Database Variable
db = SQLAlchemy()

# Initialize the SocketIO Variable
socketio = SocketIO()

# Initialize the Login Manager Variable
login_manager = LoginManager()

def create_app():
    # Create the Object of Flask
    application = Flask(__name__)

    # Load the Configuration from the config.py file
    application.config.from_object(Config)

    # Initialize the Application for the use with this Database Setup
    db.init_app(application)

    # Initialize the Application for the use with SocketIO
    socketio.init_app(application)

    # Initialize the Application for the use with the Login Manager
    login_manager.init_app(application)

    with application.app_context():
        # Import Views and Auth (Routes)
        from .views import views
        from .auth import auth

        # Register the Blueprints used in Views and Auth
        application.register_blueprint(views, url_prefix='/')
        application.register_blueprint(auth, url_prefix='/')

        # Create SQL Tables for our Data Models
        db.create_all()

        return application