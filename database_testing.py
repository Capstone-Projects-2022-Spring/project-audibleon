import unittest
from website import db
from website.models import User

class TestDatabase(unittest.TestCase):

    def test_user_model(self):

        # Create a User using the User Model to ensure the Model works as intended
        user = User(
            user_email = 'test@gmail.com',
            username = 'test-user',
            user_password = 'test-pass',
            user_phone_number = '(111)-111-1111',
            user_key_phrases = '',
            user_impairment = 1,
            audibleon_role_id = 2
        )

        self.assertEqual(user.user_email, 'test@gmail.com')
        self.assertEqual(user.username, 'test-user')
        self.assertEqual(user.user_password, 'test-pass')
        self.assertEqual(user.user_phone_number, '(111)-111-1111')
        self.assertEqual(user.user_key_phrases, '')
        self.assertEqual(user.user_impairment, 1)
        self.assertEqual(user.audibleon_role_id, 2)

    def test_password_hashing(self):

        # Create a User to test the Password Hashing used in the User Model
        user = User(
            user_email = 'test@gmail.com',
            username = 'test-user',
            user_password = 'test-pass',
            user_phone_number = '(111)-111-1111',
            user_key_phrases = '',
            user_impairment = 1,
            audibleon_role_id = 2
        )

        # Hash User Password
        hashed_password = user.set_password(user.user_password)

        # Check the Hashed Passwords Against Each Other
        self.assertEqual(hashed_password, user.user_password)

        # Check the Plaintext Password Against Each Other
        self.assertTrue(user.check_password('test-pass'))


    def test_connection(self):

        # Obtain a User from the Database. If the connection is not established this Test will Fail.
        user = User.query.filter_by(username='Xyeles').first()

        self.assertEqual(user.audibleon_user_id, 16)

if __name__ == '__main__':
    unittest.main()