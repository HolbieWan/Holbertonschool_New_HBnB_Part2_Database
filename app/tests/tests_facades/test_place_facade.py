# test_place_facade.py

import unittest
from unittest.mock import MagicMock, patch

# Import the PlaceFacade and Place classes
from app.services.facade_place import PlaceFacade
from app.models.place import Place

class TestPlaceFacade(unittest.TestCase):
    def setUp(self):
        # Create a mock place repository
        self.mock_place_repo = MagicMock()
        # Initialize the PlaceFacade with the mock repository
        self.place_facade = PlaceFacade(self.mock_place_repo)

        # Sample place data
        self.valid_place_data = {
            "title": "Cozy Cottage",
            "description": "A lovely cottage in the countryside.",
            "price": 150.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_first_name": "Alice",
            "owner_id": "user-123",
            "amenities": ["WiFi", "Fireplace"]
        }

        self.existing_place = Place(**self.valid_place_data)
        self.existing_place.id = "place-456"

    def test_create_place_success(self):
        """Test creating a place successfully."""
        # Mock get_by_attribute to return None (no existing place with the same title)
        self.mock_place_repo.get_by_attribute.return_value = None

        # Mock the Place's is_valid method to return True
        with patch.object(Place, 'is_valid', return_value=True):
            # Mock the Place's to_dict method
            with patch.object(Place, 'to_dict', return_value=self.valid_place_data):
                result = self.place_facade.create_place(self.valid_place_data)

        self.mock_place_repo.add.assert_called_once()
        self.assertEqual(result, self.valid_place_data)

    def test_create_place_existing_title(self):
        """Test creating a place with an existing title."""
        # Mock get_by_attribute to return an existing place
        self.mock_place_repo.get_by_attribute.return_value = self.existing_place

        with self.assertRaises(ValueError) as context:
            self.place_facade.create_place(self.valid_place_data)

        self.assertIn(f"Place '{self.valid_place_data['title']}' already exists. Please choose another title.", str(context.exception))

    def test_create_place_invalid_place(self):
        """Test creating a place with invalid data."""
        # Mock get_by_attribute to return None (no existing place)
        self.mock_place_repo.get_by_attribute.return_value = None

        # Mock the Place's is_valid method to return False
        with patch.object(Place, 'is_valid', return_value=False):
            with self.assertRaises(ValueError) as context:
                self.place_facade.create_place(self.valid_place_data)

        self.assertIn("Invalid place data.", str(context.exception))

    def test_get_place_success(self):
        """Test getting a place by ID successfully."""
        # Mock get to return an existing place
        self.mock_place_repo.get.return_value = self.existing_place

        # Mock the Place's to_dict method
        with patch.object(Place, 'to_dict', return_value=self.valid_place_data):
            result = self.place_facade.get_place("place-456")

        self.mock_place_repo.get.assert_called_once_with("place-456")
        self.assertEqual(result, self.valid_place_data)

    def test_get_place_not_found(self):
        """Test getting a place that does not exist."""
        # Mock get to return None (place not found)
        self.mock_place_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.place_facade.get_place("place-999")

        self.assertIn("Place with id place-999 not found.", str(context.exception))

    def test_get_all_places(self):
        """Test getting all places."""
        # Mock get_all to return a list of places
        places = [self.existing_place]
        self.mock_place_repo.get_all.return_value = places

        # Mock the Place's to_dict method
        with patch.object(Place, 'to_dict', return_value=self.valid_place_data):
            result = self.place_facade.get_all_places()

        self.mock_place_repo.get_all.assert_called_once()
        self.assertEqual(result, [self.valid_place_data])

    def test_update_place_success(self):
        """Test updating a place successfully."""
        updated_data = {
            "title": "Updated Cozy Cottage",
            "price": 175.0
        }

        # Mock get to return an existing place
        self.mock_place_repo.get.return_value = self.existing_place

        # Mock the update method
        self.mock_place_repo.update.return_value = None

        # Mock the Place's to_dict method
        updated_place_data = {**self.valid_place_data, **updated_data}
        with patch.object(Place, 'to_dict', return_value=updated_place_data):
            result = self.place_facade.update_place("place-456", updated_data)

        self.mock_place_repo.update.assert_called_once_with("place-456", updated_data)
        self.assertEqual(result["title"], "Updated Cozy Cottage")
        self.assertEqual(result["price"], 175.0)

    def test_update_place_not_found(self):
        """Test updating a place that does not exist."""
        updated_data = {
            "title": "Updated Cozy Cottage",
            "price": 175.0
        }

        # Mock get to return None (place not found)
        self.mock_place_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.place_facade.update_place("place-999", updated_data)

        self.assertIn("place with id place-999 not found.", str(context.exception))

    def test_delete_place_success(self):
        """Test deleting a place successfully."""
        # Mock get to return an existing place
        self.mock_place_repo.get.return_value = self.existing_place

        # Mock the delete method
        self.mock_place_repo.delete.return_value = None

        self.place_facade.delete_place("place-456")

        self.mock_place_repo.delete.assert_called_once_with("place-456")

    def test_delete_place_not_found(self):
        """Test deleting a place that does not exist."""
        # Mock get to return None (place not found)
        self.mock_place_repo.get.return_value = None

        with self.assertRaises(ValueError) as context:
            self.place_facade.delete_place("place-999")

        self.assertIn("Place with id: place-999 not found !", str(context.exception))

    def test_get_all_places_from_owner_id_success(self):
        """Test getting all places from an owner ID successfully."""
        # Mock get_by_attribute to return a list of places
        places = [self.existing_place]
        self.mock_place_repo.get_by_attribute.return_value = places

        # Mock the Place's to_dict method
        with patch.object(Place, 'to_dict', return_value=self.valid_place_data):
            result = self.place_facade.get_all_places_from_owner_id("user-123")

        self.mock_place_repo.get_by_attribute.assert_called_once_with("owner_id", "user-123")
        self.assertEqual(result, [self.valid_place_data])

    def test_get_all_places_from_owner_id_not_found(self):
        """Test getting places for an owner ID that has no places."""
        # Mock get_by_attribute to return None (no places found)
        self.mock_place_repo.get_by_attribute.return_value = None

        with self.assertRaises(ValueError) as context:
            self.place_facade.get_all_places_from_owner_id("user-999")

        self.assertIn("No place found for owner_id: user-999", str(context.exception))

if __name__ == '__main__':
    unittest.main()