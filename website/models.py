from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

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
        db.String(45),
        index = False,
        unique = True,
        nullable = False
    )

    user_password = db.Column(
        db.String(45),
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
        db.String(400),
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

    def __repr__(self):

        return 'User {}'.format(self.username)

    # override UserMixin get_id()
    def get_id(self):
        return self.audibleon_user_id
