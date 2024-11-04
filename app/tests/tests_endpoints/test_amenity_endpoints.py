# test_amenity_endpoints.py

import unittest
from unittest.mock import MagicMock
from flask import json

# Assuming BaseTestCase is defined in base_test.py
from app.tests.tests_endpoints.base_test import BaseTestCase

class TestAmenityEndpoints(BaseTestCase):
    def test_create_amenity(self):
        """Test creating a new amenity."""
        amenity_data = {
            "name": "Sauna"
        }

        # Mock the create_amenity method
        created_amenity = {
            "type": "amenity",
            "id": "amenity-101",
            "name": "Sauna",
            "created_at": "2022-01-02T00:00:00",
            "updated_at": "2022-01-02T00:00:00"
        }
        self.app.extensions['HBNB_FACADE'].amenity_facade.create_amenity.return_value = created_amenity

        response = self.client.post('/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'Sauna')
        self.assertEqual(data['id'], 'amenity-101')

    def test_create_amenity_invalid_data(self):
        """Test creating an amenity with invalid data."""
        amenity_data = {
            "name": ""  # Invalid name
        }

        # Mock the create_amenity method to raise ValueError
        self.app.extensions['HBNB_FACADE'].amenity_facade.create_amenity.side_effect = ValueError("Invalid amenity data")

        response = self.client.post('/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Invalid amenity data", data['message'])

    def test_get_all_amenities(self):
        """Test retrieving all amenities."""
        # Mock the get_all_amenities method
        self.app.extensions['HBNB_FACADE'].amenity_facade.get_all_amenities.return_value = [self.mock_amenity]

        response = self.client.get('/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'amenity-789')
        self.assertEqual(data[0]['name'], 'Pool')

    def test_get_amenity_by_id(self):
        """Test retrieving an amenity by ID."""
        # Mock the get_amenity method
        self.app.extensions['HBNB_FACADE'].amenity_facade.get_amenity.return_value = self.mock_amenity

        response = self.client.get('/amenities/amenity-789')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], 'amenity-789')
        self.assertEqual(data['name'], 'Pool')

    def test_get_amenity_by_id_not_found(self):
        """Test retrieving an amenity that does not exist."""
        # Mock the get_amenity method to raise ValueError
        self.app.extensions['HBNB_FACADE'].amenity_facade.get_amenity.side_effect = ValueError("Amenity not found")

        response = self.client.get('/amenities/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Amenity not found", data['message'])

    def test_update_amenity(self):
        """Test updating an amenity."""
        updated_data = {
            "name": "Updated Amenity"
        }

        updated_amenity = self.mock_amenity.copy()
        updated_amenity.update(updated_data)

        # Mock the update_amenity method
        self.app.extensions['HBNB_FACADE'].amenity_facade.update_amenity.return_value = updated_amenity

        response = self.client.put('/amenities/amenity-789', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Updated Amenity')
        self.assertEqual(data['id'], 'amenity-789')

    def test_update_amenity_not_found(self):
        """Test updating an amenity that does not exist."""
        updated_data = {
            "name": "Updated Amenity"
        }

        # Mock the update_amenity method to raise ValueError
        self.app.extensions['HBNB_FACADE'].amenity_facade.update_amenity.side_effect = ValueError("Amenity not found")

        response = self.client.put('/amenities/nonexistent', json=updated_data)
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("Amenity not found", data['message'])

    def test_delete_amenity(self):
        """Test deleting an amenity."""
        # Mock the delete_amenity method to succeed
        self.app.extensions['HBNB_FACADE'].amenity_facade.delete_amenity.return_value = None

        response = self.client.delete('/amenities/amenity-789')
        self.assertEqual(response.status_code, 200)
        data = response.get_data(as_text=True)
        self.assertIn("Amenity: amenity-789 has been deleted.", data)

    def test_delete_amenity_not_found(self):
        """Test deleting an amenity that does not exist."""
        # Mock the delete_amenity method to raise ValueError
        error_message = "Amenity with id: nonexistent not found."
        self.app.extensions['HBNB_FACADE'].amenity_facade.delete_amenity.side_effect = ValueError(error_message)

        response = self.client.delete('/amenities/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = response.get_data(as_text=True)
        self.assertIn(error_message, data)

    def test_get_all_amenities_empty(self):
        """Test retrieving all amenities when there are none."""
        # Mock the get_all_amenities method to return empty list
        self.app.extensions['HBNB_FACADE'].amenity_facade.get_all_amenities.return_value = []

        response = self.client.get('/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    unittest.main()