# test_review_endpoints.py

import unittest
from unittest.mock import MagicMock
from flask import json

# Assuming BaseTestCase is defined in base_test.py
from app.tests.tests_endpoints.base_test import BaseTestCase

class TestReviewEndpoints(BaseTestCase):
    def test_create_review(self):
        """Test creating a new review."""
        review_data = {
            "text": "Amazing place!",
            "rating": 5,
            "place_id": "place-456",
            "user_id": "user-123"
        }

        # Mock the create_review method
        created_review = self.mock_review.copy()
        created_review.update(review_data)
        created_review['id'] = 'review-101'

        self.app.extensions['HBNB_FACADE'].review_facade.create_review.return_value = created_review

        response = self.client.post('/reviews/', json=review_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], 'Amazing place!')
        self.assertEqual(data['rating'], 5)
        self.assertEqual(data['place_id'], 'place-456')
        self.assertEqual(data['user_id'], 'user-123')

    def test_create_review_invalid_data(self):
        """Test creating a review with invalid data."""
        review_data = {
            "text": "",
            "rating": 6,  # Invalid rating
            "place_id": "place-456",
            "user_id": "user-123"
        }

        # Mock the create_review method to raise ValueError
        self.app.extensions['HBNB_FACADE'].review_facade.create_review.side_effect = ValueError("Invalid review data")

        response = self.client.post('/reviews/', json=review_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Invalid review data", data['message'])

    def test_get_all_reviews(self):
        """Test retrieving all reviews."""
        # Mock the get_all_reviews method
        self.app.extensions['HBNB_FACADE'].review_facade.get_all_reviews.return_value = [self.mock_review]

        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'review-999')

    def test_get_all_reviews_empty(self):
        """Test retrieving all reviews when there are none."""
        # Mock the get_all_reviews method to return empty list
        self.app.extensions['HBNB_FACADE'].review_facade.get_all_reviews.return_value = []

        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("No review found", data['message'])

    def test_get_review_by_id(self):
        """Test retrieving a review by ID."""
        # Mock the get_review method
        self.app.extensions['HBNB_FACADE'].review_facade.get_review.return_value = self.mock_review

        response = self.client.get('/reviews/review-999')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 'review-999')
        self.assertEqual(data['text'], 'Great place to stay!')

    def test_get_review_by_id_not_found(self):
        """Test retrieving a review that does not exist."""
        # Mock the get_review method to raise ValueError
        self.app.extensions['HBNB_FACADE'].review_facade.get_review.side_effect = ValueError("Review not found")

        response = self.client.get('/reviews/nonexistent')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Review not found", data['message'])

    def test_update_review(self):
        """Test updating a review."""
        updated_data = {
            "text": "Updated review text",
            "rating": 4
        }

        updated_review = self.mock_review.copy()
        updated_review.update(updated_data)

        # Mock the update_review method
        self.app.extensions['HBNB_FACADE'].review_facade.update_review.return_value = updated_review

        response = self.client.put('/reviews/review-999', json=updated_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], 'Updated review text')
        self.assertEqual(data['rating'], 4)

    def test_update_review_not_found(self):
        """Test updating a review that does not exist."""
        updated_data = {
            "text": "Updated review text",
            "rating": 4
        }

        # Mock the update_review method to raise ValueError
        self.app.extensions['HBNB_FACADE'].review_facade.update_review.side_effect = ValueError("Review not found")

        response = self.client.put('/reviews/nonexistent', json=updated_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Review not found", data['message'])

    def test_delete_review(self):
        """Test deleting a review."""
        # Mock the get_review method
        self.app.extensions['HBNB_FACADE'].review_facade.get_review.return_value = self.mock_review

        # Mock the delete_review method
        self.app.extensions['HBNB_FACADE'].review_facade.delete_review.return_value = None

        response = self.client.delete('/reviews/review-999')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn("Review: review-999 has been deleted.", data)

    def test_delete_review_not_found(self):
        """Test deleting a review that does not exist."""
        # Mock the get_review method to raise ValueError
        self.app.extensions['HBNB_FACADE'].review_facade.get_review.side_effect = ValueError("Review not found")

        response = self.client.delete('/reviews/nonexistent')
        self.assertEqual(response.status_code, 400)
        data = response.get_data(as_text=True)
        self.assertIn("Review not fou", data)

if __name__ == '__main__':
    unittest.main()