# test_place_endpoints.py

import unittest
from unittest.mock import MagicMock
from flask import json

# Assuming BaseTestCase is defined in base_test.py
from app.tests.tests_endpoints.base_test import BaseTestCase

class TestPlaceEndpoints(BaseTestCase):
    def test_get_all_places(self):
        """Test retrieving all places."""
        # Mock the get_all_places method
        self.app.extensions['HBNB_FACADE'].place_facade.get_all_places.return_value = [self.mock_place]

        response = self.client.get('/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'place-456')
        self.assertEqual(data[0]['title'], 'Test Place')

    def test_get_all_places_empty(self):
        """Test retrieving all places when there are none."""
        # Mock the get_all_places method to return empty list
        self.app.extensions['HBNB_FACADE'].place_facade.get_all_places.return_value = []

        response = self.client.get('/places/')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("No place found", data['message'])

    def test_get_place_by_id(self):
        """Test retrieving a place by ID."""
        # Mock the get_place method
        self.app.extensions['HBNB_FACADE'].place_facade.get_place.return_value = self.mock_place

        response = self.client.get('/places/place-456')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 'place-456')
        self.assertEqual(data['title'], 'Test Place')

    def test_get_place_by_id_not_found(self):
        """Test retrieving a place that does not exist."""
        # Mock the get_place method to raise ValueError
        self.app.extensions['HBNB_FACADE'].place_facade.get_place.side_effect = ValueError("Place not found")

        response = self.client.get('/places/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Place not found", data['message'])

    def test_update_place(self):
        """Test updating a place."""
        updated_data = {
            "title": "Updated Place",
            "description": "An updated place description",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060
        }

        updated_place = self.mock_place.copy()
        updated_place.update(updated_data)

        # Mock the update_place method
        self.app.extensions['HBNB_FACADE'].place_facade.update_place.return_value = updated_place

        response = self.client.put('/places/place-456', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Place')
        self.assertEqual(data['price'], 120.0)

    def test_update_place_not_found(self):
        """Test updating a place that does not exist."""
        updated_data = {
            "title": "Updated Place",
            "description": "An updated place description",
            "price": 120.0,
            "latitude": 40.7128,
            "longitude": -74.0060
        }

        # Mock the update_place method to raise ValueError
        self.app.extensions['HBNB_FACADE'].place_facade.update_place.side_effect = ValueError("Place not found")

        response = self.client.put('/places/nonexistent', json=updated_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Place not found", data['message'])

    def test_delete_place(self):
        """Test deleting a place."""
        # Mock the delete_place_and_associated_instances method
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_place_and_associated_instances.return_value = None

        response = self.client.delete('/places/place-456')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Place: place-456 has been deleted", data['message'])

    def test_delete_place_not_found(self):
        """Test deleting a place that does not exist."""
        # Mock the delete_place_and_associated_instances method to raise ValueError
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_place_and_associated_instances.side_effect = ValueError("Place not found")

        response = self.client.delete('/places/nonexistent')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Place not found", data['message'])

    def test_add_amenity_to_place(self):
        """Test adding an amenity to a place."""
        amenity_data = {
            "name": "Sauna"
        }

        # Use a mutable dictionary for the mock return value
        return_value = {"name": "Sauna"}
        self.app.extensions['FACADE_RELATION_MANAGER'].add_amenity_to_a_place.return_value = return_value

        response = self.client.post('/places/place-456/amenities', json=amenity_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        # Assertions
        self.assertEqual(data['name'], 'Sauna')

    def test_get_all_amenities_for_place(self):
        """Test retrieving all amenities for a place."""
        # Mock the get_all_amenities_names_from_place method
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_amenities_names_from_place.return_value = ["Pool", "Sauna"]

        response = self.client.get('/places/place-456/amenities')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['place_id'], 'place-456')
        self.assertEqual(data['place_amenities'], ["Pool", "Sauna"])

    def test_delete_amenity_from_place(self):
        """Test deleting an amenity from a place."""
        # Mock the get_place method to return the mock_place
        self.app.extensions['HBNB_FACADE'].place_facade.get_place.return_value = self.mock_place

        # Mock the delete_amenity_from_place_list method
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_amenity_from_place_list.return_value = None

        response = self.client.delete('/places/place-456/amenities/Pool')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Amenity: Pool has been deleted from the place_amenities list", data['message'])

    def test_delete_amenity_not_in_place(self):
        """Test deleting an amenity that is not in the place's amenities."""
        # Mock the get_place method to return the mock_place
        self.app.extensions['HBNB_FACADE'].place_facade.get_place.return_value = self.mock_place

        response = self.client.delete('/places/place-456/amenities/NonexistentAmenity')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Amenity: NonexistentAmenity not found in the place_amenities list", data['message'])

    def test_create_review_for_place(self):
        """Test creating a review for a place."""
        review_data = {
            "user_id": "user-123",
            "text": "Great place to stay!",
            "rating": 5
        }

        # Mock the create_review_for_place method
        self.app.extensions['FACADE_RELATION_MANAGER'].create_review_for_place.return_value = self.mock_review

        response = self.client.post('/places/place-456/reviews/user-123', json=review_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], 'Great place to stay!')
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['place_id'], 'place-456')
        self.assertEqual(data['user_id'], 'user-123')

    def test_get_all_reviews_for_place(self):
        """Test retrieving all reviews for a place."""
        # Mock the get_all_reviews_dict_from_place_reviews_id_list method
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_reviews_dict_from_place_reviews_id_list.return_value = [self.mock_review]

        response = self.client.get('/places/place-456/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('reviews', data)
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual(data['reviews'][0]['id'], 'review-999')

    def test_delete_review_from_place(self):
        """Test deleting a review from a place."""
        # Mock the delete_review_from_place_list method
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_review_from_place_list.return_value = None

        response = self.client.delete('/places/place-456/review/review-999')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("Review: review-999 has been deleted from the place_reviews list", data['message'])

    def test_delete_review_not_found_in_place(self):
        """Test deleting a review that is not associated with the place."""
        # Mock the delete_review_from_place_list method to raise ValueError
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_review_from_place_list.side_effect = ValueError("Review not found in place")

        response = self.client.delete('/places/place-456/review/nonexistent-review')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Review not found in place", data['message'])

    def test_delete_place_in_user_repo(self):
        """Test deleting a place in place repo and user repo."""
        # Mock the get_place method
        self.app.extensions['HBNB_FACADE'].place_facade.get_place.return_value = self.mock_place

        # Mock the delete_place_from_owner_place_list method
        self.app.extensions['FACADE_RELATION_MANAGER'].delete_place_from_owner_place_list.return_value = None

        response = self.client.delete('/places/place-456/user')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn("Place: place-456 has been deleted", data)

    def test_delete_place_in_user_repo_not_found(self):
        """Test deleting a place that does not exist in user repo."""
        # Mock the get_place method to raise ValueError
        self.app.extensions['HBNB_FACADE'].place_facade.get_place.side_effect = ValueError("Place not found")

        response = self.client.delete('/places/nonexistent/user')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Place not found", data['message'])

    def test_get_all_places_with_specific_amenity_success(self):
        """Test retrieving all places with a specific amenity successfully."""
        amenity_name = "WiFi"
        # Mock the get_all_places_with_specifique_amenity method to return a list of places
        mock_place = {
            "id": "place-456",
            "title": "Cozy Cottage",
            "amenities": ["WiFi", "Pool"]
        }
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_places_with_specifique_amenity.return_value = [mock_place]

        response = self.client.get(f'/places/amenity/{amenity_name}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], "place-456")
        self.assertIn(amenity_name, data[0]['amenities'])

    def test_get_all_places_with_specific_amenity_not_found(self):
        """Test retrieving all places with a specific amenity when no place has it."""
        amenity_name = "NonexistentAmenity"
        # Mock the get_all_places_with_specifique_amenity method to raise ValueError
        self.app.extensions['FACADE_RELATION_MANAGER'].get_all_places_with_specifique_amenity.side_effect = ValueError(f"No place found with the amenity: {amenity_name}")

        response = self.client.get(f'/places/amenity/{amenity_name}')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn(f"No place found with the amenity: {amenity_name}", data['message'])

if __name__ == '__main__':
    unittest.main()