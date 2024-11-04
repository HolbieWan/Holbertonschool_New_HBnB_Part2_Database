# test_user_facade.py

import unittest
from unittest.mock import MagicMock, patch
from email_validator import EmailNotValidError

# Import the UserFacade and User classes
from app.services.facade_user import UserFacade
from app.models.user import User

class TestUserFacade(unittest.TestCase):
    def setUp(self):
        # Create a mock user repository
        self.mock_user_repo = MagicMock()
        # Initialize the UserFacade with the mock repository
        self.user_facade = UserFacade(self.mock_user_repo)

        # Sample user data
        self.valid_user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "is_admin": False
        }

        self.existing_user = User(**self.valid_user_data)
        self.existing_user.id = "user-123"

    def test_create_user_success(self):
        """Test creating a user successfully."""
        # Mock get_by_attribute to return None (no existing user)
        self.mock_user_repo.get_by_attribute.return_value = None

        # Mock the User's is_valid method to return True
        with patch.object(User, 'is_valid', return_value=True):
            # Mock the User's to_dict method
            with patch.object(User, 'to_dict', return_value=self.valid_user_data):
                result = self.user_facade.create_user(self.valid_user_data)

        self.mock_user_repo.add.assert_called_once()
        self.assertEqual(result, self.valid_user_data)

    def test_create_user_existing_email(self):
        """Test creating a user with an existing email."""
        # Mock get_by_attribute to return an existing user
        self.mock_user_repo.get_by_attribute.return_value = self.existing_user

        with self.assertRaises(ValueError) as context:
            self.user_facade.create_user(self.valid_user_data)

        self.assertIn(f"User with email: {self.valid_user_data['email']} already exists.", str(context.exception))

    def test_create_user_invalid_user(self):
        """Test creating a user with invalid data."""
        # Mock get_by_attribute to return None (no existing user)
        self.mock_user_repo.get_by_attribute.return_value = None

        # Mock the User's is_valid method to return False
        with patch.object(User, 'is_valid', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.user_facade.create_user(self.valid_user_data)

        self.assertIn("User validation failed. Please check the email and other attributes.", str(context.exception))

    def test_get_user_success(self):
        """Test getting a user by ID successfully."""
        # Mock get to return an existing user
        self.mock_user_repo.get.return_value = self.existing_user

        # Mock the User's to_dict method
        with patch.object(User, 'to_dict', return_value=self.valid_user_data):
            result = self.user_facade.get_user("user-123")

        self.mock_user_repo.get.assert_called_once_with("user-123")
        self.assertEqual(result, self.valid_user_data)

    def test_get_user_not_found(self):
        """Test getting a user that does not exist."""
        # Mock get to return None (user not found)
        self.mock_user_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.user_facade.get_user("user-999")

        self.assertIn("User with id user-999 not found.", str(context.exception))

    def test_get_all_users(self):
        """Test getting all users."""
        # Mock get_all to return a list of users
        users = [self.existing_user]
        self.mock_user_repo.get_all.return_value = users

        # Mock the User's to_dict method
        with patch.object(User, 'to_dict', return_value=self.valid_user_data):
            result = self.user_facade.get_all_users()

        self.mock_user_repo.get_all.assert_called_once()
        self.assertEqual(result, [self.valid_user_data])

    def test_update_user_success(self):
        """Test updating a user successfully."""
        updated_data = {
            "first_name": "Jane",
            "last_name": "Doe"
        }

        # Mock get to return an existing user
        self.mock_user_repo.get.return_value = self.existing_user

        # Mock the update method
        self.mock_user_repo.update.return_value = None

        # Mock the User's to_dict method
        with patch.object(User, 'to_dict', return_value={**self.valid_user_data, **updated_data}):
            result = self.user_facade.update_user("user-123", updated_data)

        self.mock_user_repo.update.assert_called_once_with("user-123", updated_data)
        self.assertEqual(result["first_name"], "Jane")
        self.assertEqual(result["last_name"], "Doe")

    def test_update_user_not_found(self):
        """Test updating a user that does not exist."""
        updated_data = {
            "first_name": "Jane",
            "last_name": "Doe"
        }

        # Mock get to return None (user not found)
        self.mock_user_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.user_facade.update_user("user-999", updated_data)

        self.assertIn("User with id user-999 not found.", str(context.exception))

    def test_delete_user_success(self):
        """Test deleting a user successfully."""
        # Mock get to return an existing user
        self.mock_user_repo.get.return_value = self.existing_user

        # Mock the delete method
        self.mock_user_repo.delete.return_value = None

        self.user_facade.delete_user("user-123")

        self.mock_user_repo.delete.assert_called_once_with("user-123")

    def test_delete_user_not_found(self):
        """Test deleting a user that does not exist."""
        # Mock get to return None (user not found)
        self.mock_user_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.user_facade.delete_user("user-999")

        self.assertIn("User with id user-999 not found.", str(context.exception))

    def test_create_user_invalid_email(self):
        """Test creating a user with an invalid email."""
        invalid_user_data = self.valid_user_data.copy()
        invalid_user_data["email"] = "invalid-email"

        # Mock get_by_attribute to return None (no existing user)
        self.mock_user_repo.get_by_attribute.return_value = None

        # Mock the User's is_valid method to raise EmailNotValidError
        with patch.object(User, 'is_valid', side_effect=EmailNotValidError("Invalid email format")):
            with self.assertRaises(ValueError) as context:
                self.user_facade.create_user(invalid_user_data)

        self.assertIn("Invalid email format", str(context.exception))

if __name__ == '__main__':
    unittest.main()