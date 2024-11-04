# test_amenity_facade.py

import unittest
from unittest.mock import MagicMock, patch

# Import the AmenityFacade and Amenity classes
from app.services.facade_amenity import AmenityFacade
from app.models.amenity import Amenity

class TestAmenityFacade(unittest.TestCase):
    def setUp(self):
        # Create a mock amenity repository
        self.mock_amenity_repo = MagicMock()
        # Initialize the AmenityFacade with the mock repository
        self.amenity_facade = AmenityFacade(self.mock_amenity_repo)

        # Sample amenity data
        self.valid_amenity_data = {
            "name": "Swimming Pool"
        }

        self.existing_amenity = Amenity(**self.valid_amenity_data)
        self.existing_amenity.id = "amenity-789"

    def test_create_amenity_success(self):
        """Test creating an amenity successfully."""
        # Mock get_by_attribute to return None (no existing amenity with the same name)
        self.mock_amenity_repo.get_by_attribute.return_value = None

        # Mock the Amenity's is_valid method to return True
        with patch.object(Amenity, 'is_valid', return_value=True):
            # Mock the Amenity's to_dict method
            with patch.object(Amenity, 'to_dict', return_value=self.valid_amenity_data):
                result = self.amenity_facade.create_amenity(self.valid_amenity_data)

        # self.mock_amenity_repo.add.assert_called_once()
        self.assertEqual(result, self.valid_amenity_data)

    def test_create_amenity_existing_name(self):
        """Test creating an amenity with an existing name."""
        # Mock get_by_attribute to return an existing amenity
        self.mock_amenity_repo.get_by_attribute.return_value = self.existing_amenity

        with self.assertRaises(ValueError) as context:
            self.amenity_facade.create_amenity(self.valid_amenity_data)

        self.assertIn(f"Amenity '{self.valid_amenity_data['name']}' already exists. Please choose another name.", str(context.exception))

    def test_create_amenity_invalid_data(self):
        """Test creating an amenity with invalid data."""
        # Mock get_by_attribute to return None (no existing amenity)
        self.mock_amenity_repo.get_by_attribute.return_value = None

        # Mock the Amenity's is_valid method to return False
        with patch.object(Amenity, 'is_valid', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.amenity_facade.create_amenity(self.valid_amenity_data)

        self.assertIn("Invalid amenity data.", str(context.exception))

    def test_get_amenity_success(self):
        """Test getting an amenity by ID successfully."""
        # Mock get to return an existing amenity
        self.mock_amenity_repo.get.return_value = self.existing_amenity

        # Mock the Amenity's to_dict method
        with patch.object(Amenity, 'to_dict', return_value=self.valid_amenity_data):
            result = self.amenity_facade.get_amenity("amenity-789")

        self.mock_amenity_repo.get.assert_called_once_with("amenity-789")
        self.assertEqual(result, self.valid_amenity_data)

    def test_get_amenity_not_found(self):
        """Test getting an amenity that does not exist."""
        # Mock get to return None (amenity not found)
        self.mock_amenity_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.amenity_facade.get_amenity("amenity-999")

        self.assertIn("Amenity with id: amenity-999 not found.", str(context.exception))

    def test_get_all_amenities(self):
        """Test getting all amenities."""
        # Mock get_all to return a list of amenities
        amenities = [self.existing_amenity]
        self.mock_amenity_repo.get_all.return_value = amenities

        # Mock the Amenity's to_dict method
        with patch.object(Amenity, 'to_dict', return_value=self.valid_amenity_data):
            result = self.amenity_facade.get_all_amenities()

        self.mock_amenity_repo.get_all.assert_called_once()
        self.assertEqual(result, [self.valid_amenity_data])

    def test_update_amenity_success(self):
        """Test updating an amenity successfully."""
        updated_data = {
            "name": "Updated Swimming Pool"
        }

        # Mock get to return an existing amenity
        self.mock_amenity_repo.get.return_value = self.existing_amenity

        # Mock the update method
        self.mock_amenity_repo.update.return_value = None

        # Mock the Amenity's to_dict method
        updated_amenity_data = {**self.valid_amenity_data, **updated_data}
        with patch.object(Amenity, 'to_dict', return_value=updated_amenity_data):
            result = self.amenity_facade.update_amenity("amenity-789", updated_data)

        self.mock_amenity_repo.update.assert_called_once_with("amenity-789", updated_data)
        self.assertEqual(result["name"], "Updated Swimming Pool")

    def test_update_amenity_not_found(self):
        """Test updating an amenity that does not exist."""
        updated_data = {
            "name": "Updated Swimming Pool"
        }

        # Mock get to return None (amenity not found)
        self.mock_amenity_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.amenity_facade.update_amenity("amenity-999", updated_data)

        self.assertIn("Amenity with id: amenity-999 not found.", str(context.exception))

    def test_delete_amenity_success(self):
        """Test deleting an amenity successfully."""
        # Mock get to return an existing amenity
        self.mock_amenity_repo.get.return_value = self.existing_amenity

        # Mock the delete method
        self.mock_amenity_repo.delete.return_value = None

        self.amenity_facade.delete_amenity("amenity-789")

        self.mock_amenity_repo.delete.assert_called_once_with("amenity-789")

    def test_delete_amenity_not_found(self):
        """Test deleting an amenity that does not exist."""
        # Mock get to return None (amenity not found)
        self.mock_amenity_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.amenity_facade.delete_amenity("amenity-999")

        self.assertIn("Amenity with id: amenity-999 not found.", str(context.exception))

    def test_get_all_amenitys_from_place_id_success(self):
        """Test getting all amenities from a place ID successfully."""
        # Mock get_by_attribute to return a list of amenities
        amenities = [self.existing_amenity]
        self.mock_amenity_repo.get_by_attribute.return_value = amenities

        # Mock the Amenity's to_dict method
        with patch.object(Amenity, 'to_dict', return_value=self.valid_amenity_data):
            result = self.amenity_facade.get_all_amenitys_from_place_id("place-456")

        self.mock_amenity_repo.get_by_attribute.assert_called_once_with("id", "place-456")
        self.assertEqual(result, [self.valid_amenity_data])

    def test_get_all_amenitys_from_place_id_not_found(self):
        """Test getting amenities for a place ID that has no amenities."""
        # Mock get_by_attribute to return None (no amenities found)
        self.mock_amenity_repo.get_by_attribute.return_value = None

        with self.assertRaises(ValueError) as context:
            self.amenity_facade.get_all_amenitys_from_place_id("place-999")

        self.assertIn("No amenity found for place_id: place-999", str(context.exception))

if __name__ == '__main__':
    unittest.main()