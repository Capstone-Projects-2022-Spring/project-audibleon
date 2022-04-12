from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'audibleon_user'

    audibleon_user_id = db.Column(
        db.Integer,
        primary_key = True
    )

    user_email = db.Column(
        db.String(45),
        index = True,
        unique = True,
        nullable = False
    )

    username = db.Column(
        db.String(20),
        index = False,
        unique = True,
        nullable = False
    )

    user_password = db.Column(
        db.String(200),
        index = False,
        unique = False,
        nullable = False
    )

    user_phone_number = db.Column(
        db.String(15),
        index = False,
        unique = False,
        nullable = True
    )

    user_key_phrases = db.Column(
        db.String(300),
        index = False,
        unique = False,
        nullable = True
    )

    user_impairment = db.Column(
        db.Integer,
        index = False,
        unique = False,
        nullable = False
    )

    audibleon_role_id = db.Column(
        db.Integer,
        index = False,
        unique = False,
        nullable = False
    )

    # Override the Default Properties of get_id() in UserMixin
    def get_id(self):

        return (self.audibleon_user_id)

    def get_status(self):
        return (self.user_impairment)

    def set_password(self, password):

        # Create Hashed Password
        self.user_password = generate_password_hash(
            password,
            method = 'sha256'
        )

    def check_password(self, password):

        # Check Hashed Password
        return check_password_hash(self.user_password, password)

    def __repr__(self):

        return 'User {}'.format(self.username)
