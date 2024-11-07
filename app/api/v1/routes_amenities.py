"""
routes_amenities.py

This module defines Flask routes for amenity-related operations, including 
creating, retrieving, updating, and deleting amenities.

Classes:
    AmenityList (Resource): Manages the creation of a new amenity and 
        retrieval of all amenities.
    Amenity (Resource): Handles retrieval, updating, and deletion of a specific
        amenity by ID.

Attributes:
    amenities_bp (Blueprint): Flask blueprint for amenity routes.
    api (Namespace): Namespace for amenity-related API endpoints.
    amenity_model (model): Model schema for Amenity responses.
    amenity_creation_model (model): Model schema for creating an Amenity.
"""

from flask import Blueprint, current_app, request, abort
from flask_restx import api, Namespace, Resource, fields

amenities_bp = Blueprint('amenities', __name__)
api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'type': fields.String(required=False, description='Type will be given in response', example='amenity'),
    'id': fields.String(required=False, description='Id will be given in response', example=''),
    'name': fields.String(required=True, description='Name of the amenity', example='Sauna'),
    'created_at': fields.String(required=False, description='Time of creation, given in response', example=''),
    'updated_at': fields.String(required=False, description='Time of update, given in response', example=''),
})

amenity_creation_model = api.model('Amenity_creation', {'name': fields.String(
    required=True, description='Name of the amenity', example='Sauna'), })

#   <------------------------------------------------------------------------>


@api.route('/')
class AmenityList(Resource):
    """Resource for creating a new amenity and retrieving all amenities."""

    @api.doc('create_amenity')
    @api.expect(amenity_creation_model)
    @api.marshal_with(amenity_model, code=201)  # type: ignore
    def post(self):
        """
        Creates a new amenity.

        Expects:
            JSON payload with `name` of the amenity.

        Returns:
            JSON representation of the created amenity.
        """
        facade = current_app.extensions['HBNB_FACADE']
        new_amenity = request.get_json()

        try:
            amenity = facade.amenity_facade.create_amenity(new_amenity)

            return amenity, 201

        except ValueError as e:
            abort(400, str(e))

    @api.doc('get_all_amenities')
    @api.marshal_with(amenity_model, code=201)  # type: ignore
    def get(self):
        """
        Retrieves a list of all amenities.

        Returns:
            List of amenities in JSON format.
        """
        facade = current_app.extensions['HBNB_FACADE']

        try:
            amenities = facade.amenity_facade.get_all_amenities()

            return amenities

        except ValueError as e:
            abort(400, str(e))

#   <------------------------------------------------------------------------>


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class Amenity(Resource):
    """Resource for retrieving, updating, or deleting a specific amenity by ID."""

    @api.doc('get_amenity')
    @api.marshal_with(amenity_model)  # type: ignore
    def get(self, amenity_id):
        """
        Retrieves an amenity by its unique identifier.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            JSON representation of the amenity.
        """
        facade = current_app.extensions['HBNB_FACADE']

        try:
            amenity = facade.amenity_facade.get_amenity(amenity_id)

            return amenity, 200

        except ValueError as e:
            abort(404, str(e))

    @api.doc('update_amenity')
    @api.expect(amenity_creation_model)
    @api.marshal_with(amenity_model)  # type: ignore
    def put(self, amenity_id):
        """
        Updates an existing amenity.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            JSON representation of the updated amenity.
        """
        facade = current_app.extensions['HBNB_FACADE']
        updated_data = request.get_json()

        try:
            updated_amenity = facade.amenity_facade.update_amenity(
                amenity_id, updated_data)

            return updated_amenity, 200

        except ValueError as e:
            abort(404, str(e))

    @api.doc('delete_amenity')
    def delete(self, amenity_id):
        """
        Deletes an amenity by its unique identifier.

        Args:
            amenity_id (str): The unique identifier of the amenity.

        Returns:
            Message confirming successful deletion.
        """
        facade = current_app.extensions['HBNB_FACADE']

        try:
            facade.amenity_facade.delete_amenity(amenity_id)

            return (f"Amenity: {amenity_id} has been deleted."), 200

        except ValueError as e:
            abort(404, str(e))
