import unittest
from unittest.mock import MagicMock
from flask import Flask
from flask_restx import Api

# Import your blueprints and namespaces
from app.api.v1.routes_users import users_bp, api as users_api
from app.api.v1.routes_places import places_bp, api as places_api
from app.api.v1.routes_reviews import reviews_bp, api as reviews_api
from app.api.v1.routes_amenities import amenities_bp, api as amenities_api

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        # Create a Flask application instance
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

        # Register Blueprints
        self.app.register_blueprint(users_bp, url_prefix='/users')
        self.app.register_blueprint(places_bp, url_prefix='/places')
        self.app.register_blueprint(reviews_bp, url_prefix='/reviews')
        self.app.register_blueprint(amenities_bp, url_prefix='/amenities')

        # Create an Api instance and add namespaces
        self.api = Api(self.app)
        self.api.add_namespace(users_api, path='/users')
        self.api.add_namespace(places_api, path='/places')
        self.api.add_namespace(reviews_api, path='/reviews')
        self.api.add_namespace(amenities_api, path='/amenities')

        # Create a test client
        self.client = self.app.test_client()

        # Mock current_app.extensions
        self.app.extensions = {}
        self.app.extensions['HBNB_FACADE'] = MagicMock()
        self.app.extensions['FACADE_RELATION_MANAGER'] = MagicMock()

        # Push the application context
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Mock data that can be shared across tests
        self.mock_user = {
            "type": "user",
            "id": "user-123",
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "testpassword",
            "is_admin": False,
            "places": ["place-456"],
            "created_at": "2022-01-01T00:00:00",
            "updated_at": "2022-01-01T00:00:00"
        }

        self.mock_place = {
            "type": "place",
            "id": "place-456",
            "title": "Test Place",
            "description": "A test place description",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_first_name": "Test",
            "owner_id": "user-123",
            "amenities": ["Pool"],
            "reviews": ["review-999"],
            "created_at": "2022-01-01T00:00:00",
            "updated_at": "2022-01-01T00:00:00"
        }

        self.mock_amenity = {
            "type": "amenity",
            "id": "amenity-789",
            "name": "Pool",
            "created_at": "2022-01-01T00:00:00",
            "updated_at": "2022-01-01T00:00:00"
        }

        self.mock_review = {
            "type": "review",
            "id": "review-999",
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": "place-456",
            "place_name": "Test Place",
            "user_id": "user-123",
            "user_first_name": "Test",
            "created_at": "2022-01-01T00:00:00",
            "updated_at": "2022-01-01T00:00:00"
        }

    def tearDown(self):
        """Clean up after each test."""
        self.app_context.pop()