# test_review_facade.py

import unittest
from unittest.mock import MagicMock, patch
import uuid

# Import the ReviewFacade and Review classes
from app.services.facade_review import ReviewFacade
from app.models.review import Review

class TestReviewFacade(unittest.TestCase):
    def setUp(self):
        # Create a mock review repository
        self.mock_review_repo = MagicMock()
        # Initialize the ReviewFacade with the mock repository
        self.review_facade = ReviewFacade(self.mock_review_repo)

        # Sample review data
        self.valid_review_data = {
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": "place-456",
            "place_name": "Cozy Cottage",
            "user_id": "user-123",
            "user_first_name": "John"
        }

        # Use the fixed UUID for the existing review
        fixed_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')
        self.existing_review = Review(**self.valid_review_data)
        self.existing_review.id = str(fixed_uuid)

    def test_create_review_success(self):
        """Test creating a review successfully."""
        # Mock get_by_attribute to return None (no existing review with the same id)
        self.mock_review_repo.get_by_attribute.return_value = None

        # Mock the Review's is_valid method to return True
        with patch.object(Review, 'is_valid', return_value=True):
            # Mock the Review's to_dict method
            with patch.object(Review, 'to_dict', return_value=self.valid_review_data):
                result = self.review_facade.create_review(self.valid_review_data)

        self.mock_review_repo.add.assert_called_once()
        self.assertEqual(result, self.valid_review_data)

    def test_create_review_existing_id(self):
        """Test creating a review with an existing id."""
        # Mock get_by_attribute to return an existing review
        self.mock_review_repo.get_by_attribute.return_value = self.existing_review

        fixed_uuid = uuid.UUID('12345678-1234-5678-1234-567812345678')

        # Patch 'uuid.uuid4' to return 'fixed_uuid'
        with patch('uuid.uuid4', return_value=fixed_uuid):
            with self.assertRaises(ValueError) as context:
                self.review_facade.create_review(self.valid_review_data)

        expected_message = f"Review: {fixed_uuid}' already exists. Please create a new review."
        self.assertIn(expected_message, str(context.exception))

    def test_create_review_invalid_data(self):
        """Test creating a review with invalid data."""
        # Mock get_by_attribute to return None (no existing review)
        self.mock_review_repo.get_by_attribute.return_value = None

        # Mock the Review's is_valid method to return False
        with patch.object(Review, 'is_valid', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.review_facade.create_review(self.valid_review_data)

        self.assertIn("Invalid review data.", str(context.exception))

    def test_get_all_reviews(self):
        """Test getting all reviews."""
        # Mock get_all to return a list of reviews
        reviews = [self.existing_review]
        self.mock_review_repo.get_all.return_value = reviews

        # Mock the Review's to_dict method
        with patch.object(Review, 'to_dict', return_value=self.valid_review_data):
            result = self.review_facade.get_all_reviews()

        self.mock_review_repo.get_all.assert_called_once()
        self.assertEqual(result, [self.valid_review_data])

    def test_get_review_success(self):
        """Test getting a review by ID successfully."""
        # Mock get to return an existing review
        self.mock_review_repo.get.return_value = self.existing_review

        # Mock the Review's to_dict method
        with patch.object(Review, 'to_dict', return_value=self.valid_review_data):
            result = self.review_facade.get_review("review-999")

        self.mock_review_repo.get.assert_called_once_with("review-999")
        self.assertEqual(result, self.valid_review_data)

    def test_get_review_not_found(self):
        """Test getting a review that does not exist."""
        # Mock get to return None (review not found)
        self.mock_review_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.review_facade.get_review("review-999")

        self.assertIn("Review: review-999 does not exist !", str(context.exception))

    def test_update_review_success(self):
        """Test updating a review successfully."""
        updated_data = {
            "text": "Updated review text",
            "rating": 4
        }

        # Mock get to return an existing review
        self.mock_review_repo.get.return_value = self.existing_review

        # Mock the update method
        self.mock_review_repo.update.return_value = None

        # Mock the Review's to_dict method
        updated_review_data = {**self.valid_review_data, **updated_data}
        with patch.object(Review, 'to_dict', return_value=updated_review_data):
            result = self.review_facade.update_review("review-999", updated_data)

        self.mock_review_repo.update.assert_called_once_with("review-999", updated_data)
        self.assertEqual(result["text"], "Updated review text")
        self.assertEqual(result["rating"], 4)

    def test_update_review_not_found(self):
        """Test updating a review that does not exist."""
        updated_data = {
            "text": "Updated review text",
            "rating": 4
        }

        # Mock get to return None (review not found)
        self.mock_review_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.review_facade.update_review("review-999", updated_data)

        self.assertIn("Review: review-999 not found", str(context.exception))

    def test_delete_review_success(self):
        """Test deleting a review successfully."""
        # Mock get to return an existing review
        self.mock_review_repo.get.return_value = self.existing_review

        # Mock the delete method
        self.mock_review_repo.delete.return_value = None

        self.review_facade.delete_review("review-999")

        self.mock_review_repo.delete.assert_called_once_with("review-999")

    def test_delete_review_not_found(self):
        """Test deleting a review that does not exist."""
        # Mock get to return None (review not found)
        self.mock_review_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.review_facade.delete_review("review-999")

        self.assertIn("Review: review-999 not found !", str(context.exception))

if __name__ == '__main__':
    unittest.main()