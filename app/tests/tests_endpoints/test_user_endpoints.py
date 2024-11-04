import unittest
from unittest.mock import MagicMock
from flask import json

from app.tests.tests_endpoints.base_test import BaseTestCase

class TestUserEndpoints(BaseTestCase):
    # def test_home_route(self):
    #     """Test the home route."""
    #     response = self.client.get('/users/home')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.get_data(as_text=True), 'Welcome to the homepage')

    def test_create_user(self):
        """Test creating a new user."""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "testpassword",
            "is_admin": False
        }

        # Mock the create_user method
        self.app.extensions['HBNB_FACADE'].user_facade.create_user.return_value = self.mock_user

        response = self.client.post('/users/', json=user_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['email'], 'test.user@example.com')
        self.assertEqual(data['password'], '****')  # Password should be masked
        self.assertEqual(data['is_admin'], False)
        self.assertEqual(data['places'], [""])
        self.assertEqual(data['created_at'], "")
        self.assertEqual(data['updated_at'], "")

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data."""
        user_data = {
            "first_name": "",
            "last_name": "User",
            "email": "invalid-email",
            "password": "testpassword",
            "is_admin": False
        }

        # Mock the create_user method to raise ValueError
        self.app.extensions['HBNB_FACADE'].user_facade.create_user.side_effect = ValueError("Invalid user data")

        response = self.client.post('/users/', json=user_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Invalid user data", data['message'])

    def test_get_all_users(self):
        """Test retrieving all users."""
        # Mock the get_all_users method
        self.app.extensions['HBNB_FACADE'].user_facade.get_all_users.return_value = [self.mock_user]

        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'user-123')

    def test_get_all_users_empty(self):
        """Test retrieving all users when there are none."""
        # Mock the get_all_users method to return empty list
        self.app.extensions['HBNB_FACADE'].user_facade.get_all_users.return_value = []

        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("No user found", data['message'])

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        # Mock the get_user method
        self.app.extensions['HBNB_FACADE'].user_facade.get_user.return_value = self.mock_user

        response = self.client.get('/users/user-123')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 'user-123')
        self.assertEqual(data['first_name'], 'Test')

    def test_get_user_by_id_not_found(self):
        """Test retrieving a user that does not exist."""
        # Mock the get_user method to raise ValueError
        self.app.extensions['HBNB_FACADE'].user_facade.get_user.side_effect = ValueError("User not found")

        response = self.client.get('/users/nonexistent')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("User not found", data['message'])

    def test_update_user(self):
        """Test updating a user."""
        updated_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated.user@example.com"
        }

        updated_user = self.mock_user.copy()
        updated_user.update(updated_data)

        # Mock the update_user method
        self.app.extensions['HBNB_FACADE'].user_facade.update_user.return_value = updated_user

        response = self.client.put('/users/user-123', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Updated')
        self.assertEqual(data['email'], 'updated.user@example.com')

    def test_update_user_not_found(self):
        """Test updating a user that does not exist."""
        updated_data = {
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated.user@example.com"
        }

        # Mock the update_user method to raise ValueError
        self.app.extensions['HBNB_FACADE'].user_facade.update_user.side_effect = ValueError("User not found")

        response = self.client.put('/users/nonexistent', json=updated_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("User not found", data['message'])

    def test_delete_user(self):
        """Test deleting a user."""
        # Mock the delete_user_and_associated_instances method
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_user_and_associated_instances.return_value = None

        response = self.client.delete('/users/user-123')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("User: user-123 has been deleted", data['message'])

    def test_delete_user_not_found(self):
        """Test deleting a user that does not exist."""
        # Mock the delete_user_and_associated_instances method to raise ValueError
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_user_and_associated_instances.side_effect = ValueError("User not found")

        response = self.client.delete('/users/nonexistent')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("User not found", data['message'])

    def test_create_place_for_user(self):
        """Test creating a place for a user."""
        place_data = {
            "title": "New Place",
            "description": "A new place description",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": "user-123"
        }

        # Mock the created place data
        new_place = self.mock_place.copy()
        new_place.update(place_data)
        new_place['id'] = 'place-789'

        # Mock the create_place_for_user method
        self.app.extensions['FACADE_RELATION_MANAGER'].create_place_for_user.return_value = new_place

        response = self.client.post('/users/user-123/place', json=place_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'New Place')
        self.assertEqual(data['owner_id'], 'user-123')

    def test_create_place_for_user_not_found(self):
        """Test creating a place for a user that does not exist."""
        place_data = {
            "title": "New Place",
            "description": "A new place description",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": "nonexistent"
        }

        # Mock the create_place_for_user method to raise ValueError
        self.app.extensions['FACADE_RELATION_MANAGER'].create_place_for_user.side_effect = ValueError("User not found")

        response = self.client.post('/users/nonexistent/place', json=place_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("User not found", data['message'])

    def test_get_places_by_user_id(self):
        """Test retrieving all places from the user_id."""
        places = [self.mock_place]

        # Mock the get_all_places_from_owner_id method
        self.app.extensions['HBNB_FACADE'].place_facade.get_all_places_from_owner_id.return_value = places

        response = self.client.get('/users/user-123/place')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('places', data)
        self.assertEqual(len(data['places']), 1)
        self.assertEqual(data['places'][0]['id'], 'place-456')

    def test_get_places_by_user_id_not_found(self):
        """Test retrieving places for a user that does not exist."""
        # Mock the get_all_places_from_owner_id method to raise ValueError
        self.app.extensions['HBNB_FACADE'].place_facade.get_all_places_from_owner_id.side_effect = ValueError("No places found for user")

        response = self.client.get('/users/nonexistent/place')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("No places found for user", data['message'])

    def test_get_places_by_user_id_no_places(self):
        """Test retrieving places for a user with no places."""
        # Mock the get_all_places_from_owner_id method to return empty list
        self.app.extensions['HBNB_FACADE'].place_facade.get_all_places_from_owner_id.return_value = []

        response = self.client.get('/users/user-123/place')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('places', data)
        self.assertEqual(len(data['places']), 0)


    def test_get_all_reviews_from_user_success(self):
        """Test retrieving all reviews from a user successfully."""
        user_id = "user-123"
        # Mock the get_all_reviews_from_user method to return a list of reviews
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_reviews_from_user.return_value = [
            {"id": "review-789", "text": "Great place!", "rating": 5, "place_id": "place-456", "user_id": user_id}
        ]

        response = self.client.get(f'/users/{user_id}/reviews')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'review-789')
        self.assertEqual(data[0]['text'], 'Great place!')
        self.assertEqual(data[0]['rating'], 5)
        self.assertEqual(data[0]['user_id'], user_id)

    def test_get_all_reviews_from_user_user_not_found(self):
        """Test retrieving reviews for a user that does not exist."""
        user_id = "nonexistent"
        # Mock the get_all_reviews_from_user method to raise ValueError
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_reviews_from_user.side_effect = ValueError("This user does not exist")

        response = self.client.get(f'/users/{user_id}/reviews')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("This user does not exist", data['message'])

    def test_get_all_reviews_from_user_no_reviews(self):
        """Test retrieving reviews for a user with no reviews."""
        user_id = "user-123"
        # Mock the get_all_reviews_from_user method to raise ValueError for no reviews
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_reviews_from_user.side_effect = ValueError(f"No review found for this user: {user_id}")

        response = self.client.get(f'/users/{user_id}/reviews')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn(f"No review found for this user: {user_id}", data['message'])

if __name__ == '__main__':
    unittest.main()