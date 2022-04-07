from flask import Flask
from .config import Config
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
db = SQLAlchemy()


def create_app(debug):
    # Create the Object of Flask
    app = Flask(__name__)
    app.debug=debug

    # Load the Configuration from the config.py file
    app.config.from_object(Config)

    # Initialize the Application for the use with this Database Setup
    db.init_app(app)

    with app.app_context():
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)
        # # Import Views and Auth (Routes)
        # from app.main.views import main
        # from app.main.auth import main
        #
        # # Register the Blueprints used in Views and Auth
        # app.register_blueprint(main, url_prefix='/')
        # app.register_blueprint(main, url_prefix='/')

        # Create SQL Tables for our Data Models
        db.create_all()

        socketio.init_app(app)

        return app