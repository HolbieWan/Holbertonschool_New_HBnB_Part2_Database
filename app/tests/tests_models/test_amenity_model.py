import unittest
from app.models.amenity import Amenity

class TestAmenityModel(unittest.TestCase):

    def test_amenity_creation_valid(self):
        """Test creating an amenity with valid data."""
        amenity = Amenity(name='Swimming Pool')
        self.assertEqual(amenity.name, 'Swimming Pool')
        self.assertIsNotNone(amenity.id)
        self.assertIsNotNone(amenity.created_at)
        self.assertIsNotNone(amenity.updated_at)

    def test_is_valid_with_valid_data(self):
        """Test that is_valid returns True for valid amenity data."""
        amenity = Amenity(name='Wi-Fi')
        self.assertTrue(amenity.is_valid())

    def test_is_valid_with_non_string_name(self):
        """Test that is_valid returns False when name is not a string."""
        amenity = Amenity(name=12345)
        self.assertFalse(amenity.is_valid())

    def test_is_valid_with_empty_name(self):
        """Test that is_valid returns False when name is empty."""
        amenity = Amenity(name='')
        self.assertFalse(amenity.is_valid())

    def test_is_valid_with_long_name(self):
        """Test that is_valid returns False when name exceeds 50 characters."""
        amenity = Amenity(name='A' * 51)
        self.assertFalse(amenity.is_valid())

    def test_to_dict(self):
        """Test that to_dict returns a correct dictionary representation."""
        amenity = Amenity(name='Gym')
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict['type'], 'amenity')
        self.assertEqual(amenity_dict['id'], amenity.id)
        self.assertEqual(amenity_dict['name'], 'Gym')
        self.assertEqual(amenity_dict['created_at'], amenity.created_at.isoformat())
        self.assertEqual(amenity_dict['updated_at'], amenity.updated_at.isoformat())

    def test_is_valid_with_name_length_50(self):
        """Test that is_valid returns True when name length is exactly 50."""
        amenity = Amenity(name='A' * 50)
        self.assertTrue(amenity.is_valid())

    def test_is_valid_with_name_none(self):
        """Test that is_valid returns False when name is None."""
        amenity = Amenity(name=None)
        self.assertFalse(amenity.is_valid())

    def test_amenity_creation_missing_name(self):
        """Test that creating an amenity without a name raises TypeError."""
        with self.assertRaises(TypeError):
            Amenity() # type: ignore

    def test_is_valid_with_special_characters_in_name(self):
        """Test that is_valid returns True when name contains special characters."""
        amenity = Amenity(name='Spa & Wellness')
        self.assertTrue(amenity.is_valid())

    def test_is_valid_with_whitespace_name(self):
        """Test that is_valid returns False when name is whitespace."""
        amenity = Amenity(name='   ')
        self.assertFalse(amenity.is_valid())

    def test_is_valid_with_numeric_string_name(self):
        """Test that is_valid returns True when name is a numeric string."""
        amenity = Amenity(name='1234567890')
        self.assertTrue(amenity.is_valid())

    def test_is_valid_with_unicode_characters_in_name(self):
        """Test that is_valid returns True when name contains Unicode characters."""
        amenity = Amenity(name='Café')
        self.assertTrue(amenity.is_valid())

    def test_to_dict_contains_all_keys(self):
        """Test that to_dict contains all expected keys."""
        amenity = Amenity(name='Parking')
        amenity_dict = amenity.to_dict()
        expected_keys = {'type', 'id', 'name', 'created_at', 'updated_at'}
        self.assertEqual(set(amenity_dict.keys()), expected_keys)

    def test_updated_at_changes_on_name_change(self):
        """Test that updated_at changes when the name is updated."""
        amenity = Amenity(name='Original Name')
        original_updated_at = amenity.updated_at
        amenity.name = 'Updated Name'
        amenity.save()  # Assuming save() method updates updated_at
        self.assertNotEqual(amenity.updated_at, original_updated_at)

if __name__ == '__main__':
    unittest.main()