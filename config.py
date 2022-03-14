import os



class Config(object):

    # Secret Key Configuration (Either uses Environment Variable or a Hard Coded String)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'as;dlfkja;sdlkjf'

    # Obtain Username, Password, and Database Name from Environment Variables
    #db_username = os.environ.get('DB_USER')
    #db_password = os.environ.get('DB_PASS')
    #db_name = os.environ.get('DB_NAME')
    db_username = os.environ.get('AWS_DB_USER')
    db_password = os.environ.get('AWS_DB_PASS')
    db_endpoint = os.environ.get('AWS_DB_ENDPOINT')
    db_name = os.environ.get('AWS_DB_NAME')

    # SQLAlchemy Database Configuration
    #SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_username}:{db_password}@localhost:3307/{db_name}'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_username}:{db_password}@{db_endpoint}:3306/{db_name}'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
