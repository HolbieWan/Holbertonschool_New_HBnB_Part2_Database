import unittest
from app.models.user import User
from email_validator import EmailNotValidError

class TestUserModel(unittest.TestCase):
    def test_user_creation_valid(self):
        """Test creating a user with valid data."""
        user = User(
            first_name='John',
            last_name='Doe',
            email='john.doe@gmail.com',
            password='password123',
            is_admin=False
        )
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john.doe@gmail.com')
        self.assertEqual(user.password, 'password123')
        self.assertFalse(user.is_admin)
        self.assertEqual(user.places, [])

    def test_is_valid_with_valid_data(self):
        """Test that is_valid returns True for valid user data."""
        user = User(
            first_name='Alice',
            last_name='Smith',
            email='alice.smith@gmail.com',
            password='securepass'
        )
        self.assertTrue(user.is_valid())

    def test_is_valid_with_invalid_email(self):
        """Test that is_valid raises ValueError for invalid email."""
        user = User(
            first_name='Bob',
            last_name='Brown',
            email='invalid-email',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('Email validation failed', str(context.exception))

    def test_is_valid_with_empty_first_name(self):
        """Test that is_valid raises ValueError for empty first_name."""
        user = User(
            first_name='',
            last_name='Brown',
            email='bob.brown@gmail.com',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('first_name and last_name must not be empty', str(context.exception))

    def test_is_valid_with_long_first_name(self):
        """Test that is_valid raises ValueError for first_name over 50 characters."""
        user = User(
            first_name='A' * 51,
            last_name='Brown',
            email='bob.brown@gmail.com',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('first_name and last_name must not be empty', str(context.exception))

    def test_is_valid_with_non_string_attributes(self):
        """Test that is_valid raises ValueError when attributes are not strings."""
        user = User(
            first_name=123,
            last_name='Brown',
            email='bob.brown@gmail.com',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('Type error', str(context.exception))

    def test_is_valid_with_none_email(self):
        """Test that is_valid raises ValueError when email is None."""
        user = User(
            first_name='Charlie',
            last_name='Davis',
            email=None,
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('Type error', str(context.exception))

    def test_to_dict(self):
        """Test that to_dict returns a correct dictionary representation."""
        user = User(
            first_name='Diana',
            last_name='Evans',
            email='diana.evans@gmail.com',
            password='mypassword',
            is_admin=True
        )
        user_dict = user.to_dict()
        self.assertEqual(user_dict['type'], 'user')
        self.assertEqual(user_dict['first_name'], 'Diana')
        self.assertEqual(user_dict['last_name'], 'Evans')
        self.assertEqual(user_dict['email'], 'diana.evans@gmail.com')
        self.assertEqual(user_dict['password'], 'mypassword')
        self.assertTrue(user_dict['is_admin'])
        self.assertEqual(user_dict['places'], [])
        self.assertIsNotNone(user_dict['id'])
        self.assertIsNotNone(user_dict['created_at'])
        self.assertIsNotNone(user_dict['updated_at'])

    # def test_add_place(self):
    #     """Test that add_place correctly adds a place to the user's places list."""
    #     user = User(
    #         first_name='Eve',
    #         last_name='Foster',
    #         email='eve.foster@gmail.com',
    #         password='password123'
    #     )
    #     place_id = 'place-123'
    #     user.add(place_id)
    #     self.assertIn(place_id, user.places)

    def test_user_creation_missing_arguments(self):
        """Test that creating a user without required arguments raises TypeError."""
        with self.assertRaises(TypeError):
            User(
                first_name='Frank',
                last_name='Green',
                password='password123'
                # Missing email argument
            ) # type: ignore

    def test_is_valid_with_empty_last_name(self):
        """Test that is_valid raises ValueError for empty last_name."""
        user = User(
            first_name='Grace',
            last_name='',
            email='grace.hill@gmail.com',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('first_name and last_name must not be empty', str(context.exception))

    def test_is_valid_with_long_last_name(self):
        """Test that is_valid raises ValueError for last_name over 50 characters."""
        user = User(
            first_name='Henry',
            last_name='B' * 51,
            email='henry.jones@gmail.com',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('first_name and last_name must not be empty', str(context.exception))

    def test_is_valid_with_non_string_password(self):
        """Test that is_valid raises ValueError when password is not a string."""
        user = User(
            first_name='Ivy',
            last_name='King',
            email='ivy.king@gmail.com',
            password=123456
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('Type error', str(context.exception))

    def test_is_valid_with_first_name_length_50(self):
        """Test that is_valid returns True when first_name length is exactly 50."""
        user = User(
            first_name='A' * 50,
            last_name='Lewis',
            email='jane.lewis@gmail.com',
            password='password123'
        )
        self.assertTrue(user.is_valid())

    def test_is_valid_with_first_name_none(self):
        """Test that is_valid raises ValueError when first_name is None."""
        user = User(
            first_name=None,
            last_name='Martin',
            email='jane.martin@gmail.com',
            password='password123'
        )
        with self.assertRaises(ValueError) as context:
            user.is_valid()
        self.assertIn('Type error', str(context.exception))

if __name__ == '__main__':
    unittest.main()