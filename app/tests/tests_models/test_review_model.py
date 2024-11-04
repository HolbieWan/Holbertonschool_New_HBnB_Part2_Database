import unittest
from app.models.review import Review

class TestReviewModel(unittest.TestCase):

    def test_review_creation_valid(self):
        """Test creating a review with valid data."""
        review = Review(
            text='Great place to stay!',
            rating=5,
            place_id='place-123',
            place_name='Seaside Villa',
            user_id='user-456',
            user_first_name='Alice'
        )
        self.assertEqual(review.text, 'Great place to stay!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place_id, 'place-123')
        self.assertEqual(review.place_name, 'Seaside Villa')
        self.assertEqual(review.user_id, 'user-456')
        self.assertEqual(review.user_first_name, 'Alice')
        self.assertIsNotNone(review.id)
        self.assertIsNotNone(review.created_at)
        self.assertIsNotNone(review.updated_at)

    def test_is_valid_with_valid_data(self):
        """Test that is_valid returns True for valid review data."""
        review = Review(
            text='Amazing experience!',
            rating=4,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertTrue(review.is_valid())

    def test_is_valid_with_non_string_text(self):
        """Test that is_valid returns False when text is not a string."""
        review = Review(
            text=12345,
            rating=4,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

    def test_is_valid_with_non_int_rating(self):
        """Test that is_valid returns False when rating is not an integer."""
        review = Review(
            text='Good place',
            rating='5',
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

    def test_is_valid_with_rating_out_of_range(self):
        """Test that is_valid returns False when rating is out of range."""
        # Rating less than 1
        review = Review(
            text='Not good',
            rating=0,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

        # Rating greater than 5
        review.rating = 6
        self.assertFalse(review.is_valid())

    def test_is_valid_with_empty_text(self):
        """Test that is_valid returns False when text is empty."""
        review = Review(
            text='',
            rating=3,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

    def test_is_valid_with_empty_place_name(self):
        """Test that is_valid returns False when place_name is empty."""
        review = Review(
            text='Nice stay',
            rating=4,
            place_id='place-789',
            place_name='',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

    def test_is_valid_with_empty_place_id(self):
        """Test that is_valid returns False when place_id is empty."""
        review = Review(
            text='Nice stay',
            rating=4,
            place_id='',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

    def test_is_valid_with_empty_user_id(self):
        """Test that is_valid returns False when user_id is empty."""
        review = Review(
            text='Nice stay',
            rating=4,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='',
            user_first_name='Bob'
        )
        self.assertFalse(review.is_valid())

    def test_is_valid_with_empty_user_first_name(self):
        """Test that is_valid returns False when user_first_name is empty."""
        review = Review(
            text='Nice stay',
            rating=4,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name=''
        )
        self.assertFalse(review.is_valid())

    def test_to_dict(self):
        """Test that to_dict returns a correct dictionary representation."""
        review = Review(
            text='Lovely place!',
            rating=5,
            place_id='place-789',
            place_name='Mountain Cabin',
            user_id='user-321',
            user_first_name='Bob'
        )
        review_dict = review.to_dict()
        self.assertEqual(review_dict['type'], 'review')
        self.assertEqual(review_dict['id'], review.id)
        self.assertEqual(review_dict['text'], 'Lovely place!')
        self.assertEqual(review_dict['rating'], 5)
        self.assertEqual(review_dict['place_id'], 'place-789')
        self.assertEqual(review_dict['place_name'], 'Mountain Cabin')
        self.assertEqual(review_dict['user_id'], 'user-321')
        self.assertEqual(review_dict['user_first_name'], 'Bob')
        self.assertEqual(review_dict['created_at'], review.created_at.isoformat())
        self.assertEqual(review_dict['updated_at'], review.updated_at.isoformat())

if __name__ == '__main__':
    unittest.main()