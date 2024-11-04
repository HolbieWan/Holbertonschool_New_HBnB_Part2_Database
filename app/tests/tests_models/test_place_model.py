import unittest
from app.models.place import Place

class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test."""
        # Clear the mutable default arguments to prevent shared state between tests
        if Place.__init__.__defaults__:
            default_amenities, default_reviews = Place.__init__.__defaults__


    def test_place_creation_valid(self):
        """Test creating a place with valid data."""
        place = Place(
            title='Lovely Cottage',
            description='A cozy cottage in the woods.',
            price=150.0,
            latitude=45.0,
            longitude=-75.0,
            owner_id='owner-123',
            owner_first_name='Alice',
            amenities=[],
            reviews=[]
        )
        self.assertEqual(place.title, 'Lovely Cottage')
        self.assertEqual(place.description, 'A cozy cottage in the woods.')
        self.assertEqual(place.price, 150.0)
        self.assertEqual(place.latitude, 45.0)
        self.assertEqual(place.longitude, -75.0)
        self.assertEqual(place.owner_id, 'owner-123')
        self.assertEqual(place.owner_first_name, 'Alice')
        self.assertEqual(place.reviews, [])
        self.assertEqual(place.amenities, [])

    def test_is_valid_with_valid_data(self):
        """Test that is_valid returns True for valid place data."""
        place = Place(
            title='Seaside Villa',
            description='Beautiful villa by the sea.',
            price=250.0,
            latitude=36.5,
            longitude=-121.9,
            owner_id='owner-456',
            owner_first_name='Bob',
            amenities=[],
            reviews=[]
        )
        self.assertTrue(place.is_valid())

    def test_is_valid_with_non_string_title(self):
        """Test that is_valid returns False when title is not a string."""
        place = Place(
            title=123,
            description='A nice place.',
            price=100.0,
            latitude=30.0,
            longitude=120.0,
            owner_id='owner-789',
            owner_first_name='Carol',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_negative_price(self):
        """Test that is_valid returns False when price is negative."""
        place = Place(
            title='Mountain Cabin',
            description='Cozy cabin in the mountains.',
            price=-50.0,
            latitude=40.0,
            longitude=-105.0,
            owner_id='owner-101',
            owner_first_name='Dave',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_long_title(self):
        """Test that is_valid returns False when title exceeds 100 characters."""
        place = Place(
            title='A' * 101,
            description='An excessively titled place.',
            price=80.0,
            latitude=35.0,
            longitude=139.0,
            owner_id='owner-202',
            owner_first_name='Eve',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_non_float_price_lat_long(self):
        """Test that is_valid returns False when price, latitude, or longitude is not a float."""
        place = Place(
            title='Urban Flat',
            description='Modern flat in the city center.',
            price='200',
            latitude='50.0',
            longitude='0.0',
            owner_id='owner-303',
            owner_first_name='Frank',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_invalid_latitude(self):
        """Test that is_valid returns False when latitude is out of range."""
        place = Place(
            title='North Pole Station',
            description='A station at the North Pole.',
            price=300.0,
            latitude=95.0,  # Invalid latitude
            longitude=0.0,
            owner_id='owner-404',
            owner_first_name='Grace',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_invalid_longitude(self):
        """Test that is_valid returns False when longitude is out of range."""
        place = Place(
            title='International Date Line',
            description='A place on the date line.',
            price=200.0,
            latitude=0.0,
            longitude=190.0,  # Invalid longitude
            owner_id='owner-505',
            owner_first_name='Heidi',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_add_review(self):
        """Test that add_review correctly adds a review to the place."""
        place = Place(
            title='Beach House',
            description='A house on the beach.',
            price=400.0,
            latitude=25.0,
            longitude=-80.0,
            owner_id='owner-606',
            owner_first_name='Ivan',
            amenities=[],
            reviews=[]
        )
        review_id = 'review-1'
        place.add_review(review_id)
        self.assertIn(review_id, place.reviews)

    def test_add_amenity(self):
        """Test that add_amenity correctly adds an amenity to the place."""
        place = Place(
            title='Lake House',
            description='A house by the lake.',
            price=350.0,
            latitude=44.0,
            longitude=-93.0,
            owner_id='owner-707',
            owner_first_name='Judy',
            amenities=[],
            reviews=[]
        )
        amenity_name = 'Hot Tub'
        place.add_amenity(amenity_name)
        self.assertIn(amenity_name, place.amenities)

    def test_to_dict(self):
        """Test that to_dict returns a correct dictionary representation."""
        place = Place(
            title='City Apartment',
            description='An apartment in the city.',
            price=220.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id='owner-808',
            owner_first_name='Kevin',
            amenities=[],
            reviews=[]
        )
        place_dict = place.to_dict()
        self.assertEqual(place_dict['type'], 'place')
        self.assertEqual(place_dict['title'], 'City Apartment')
        self.assertEqual(place_dict['description'], 'An apartment in the city.')
        self.assertEqual(place_dict['price'], 220.0)
        self.assertEqual(place_dict['latitude'], 40.7128)
        self.assertEqual(place_dict['longitude'], -74.0060)
        self.assertEqual(place_dict['owner_id'], 'owner-808')
        self.assertEqual(place_dict['owner_first_name'], 'Kevin')
        self.assertEqual(place_dict['reviews'], [])
        self.assertEqual(place_dict['amenities'], [])
        self.assertIsNotNone(place_dict['id'])
        self.assertIsNotNone(place_dict['created_at'])
        self.assertIsNotNone(place_dict['updated_at'])

    def test_is_valid_with_missing_arguments(self):
        """Test that creating a place with missing arguments raises TypeError."""
        with self.assertRaises(TypeError):
            Place(
                title='Missing Fields',
                description='Some fields are missing.',
                price=100.0,
                latitude=20.0,
                longitude=30.0,
                # Missing owner_id and owner_first_name
                amenities=[],
                reviews=[]
            ) # type: ignore

    def test_is_valid_with_price_zero(self):
        """Test that is_valid returns True when price is zero."""
        place = Place(
            title='Free Stay',
            description='A place with no cost.',
            price=0.0,
            latitude=50.0,
            longitude=0.0,
            owner_id='owner-909',
            owner_first_name='Laura',
            amenities=[],
            reviews=[]
        )
        self.assertTrue(place.is_valid())

    def test_is_valid_with_price_not_number(self):
        """Test that is_valid returns False when price is not a number."""
        place = Place(
            title='Invalid Price',
            description='Price is not a number.',
            price='free',
            latitude=50.0,
            longitude=0.0,
            owner_id='owner-010',
            owner_first_name='Mike',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_latitude_not_number(self):
        """Test that is_valid returns False when latitude is not a number."""
        place = Place(
            title='Invalid Latitude',
            description='Latitude is not a number.',
            price=100.0,
            latitude='north',
            longitude=0.0,
            owner_id='owner-111',
            owner_first_name='Nina',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_longitude_not_number(self):
        """Test that is_valid returns False when longitude is not a number."""
        place = Place(
            title='Invalid Longitude',
            description='Longitude is not a number.',
            price=100.0,
            latitude=0.0,
            longitude='east',
            owner_id='owner-222',
            owner_first_name='Oscar',
            amenities=[],
            reviews=[]
        )
        self.assertFalse(place.is_valid())

    def test_is_valid_with_latitude_edge_values(self):
        """Test that is_valid returns True for latitude at edge values."""
        place = Place(
            title='South Pole Station',
            description='A station at the South Pole.',
            price=500.0,
            latitude=-90.0,
            longitude=0.0,
            owner_id='owner-333',
            owner_first_name='Paul',
            amenities=[],
            reviews=[]
        )
        self.assertTrue(place.is_valid())

        place.latitude = 90.0
        self.assertTrue(place.is_valid())

    def test_is_valid_with_longitude_edge_values(self):
        """Test that is_valid returns True for longitude at edge values."""
        place = Place(
            title='Date Line West',
            description='Place at the International Date Line West.',
            price=200.0,
            latitude=0.0,
            longitude=-180.0,
            owner_id='owner-444',
            owner_first_name='Quincy',
            amenities=[],
            reviews=[]
        )
        self.assertTrue(place.is_valid())

        place.longitude = 180.0
        self.assertTrue(place.is_valid())

    def test_is_valid_with_title_length_100(self):
        """Test that is_valid returns True when title length is exactly 100."""
        place = Place(
            title='A' * 100,
            description='A place with a very long title.',
            price=120.0,
            latitude=30.0,
            longitude=30.0,
            owner_id='owner-555',
            owner_first_name='Rachel',
            amenities=[],
            reviews=[]
        )
        self.assertTrue(place.is_valid())

if __name__ == '__main__':
    unittest.main()