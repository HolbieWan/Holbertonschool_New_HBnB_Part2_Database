"""
routes_places.py

This module defines Flask routes for place-related operations, such as creating,
retrieving, updating, and deleting places. It also includes routes for managing
related resources, like amenities and reviews associated with each place.

Classes:
    PlaceList (Resource): Manages retrieval of all places.
    PlaceResource (Resource): Handles retrieval, updating, and deletion of a
        specific place.
    PlaceUserOwnerDetails (Resource): Deletes a place from both place and user
        repositories.
    AmenityPlaceList (Resource): Manages amenities associated with a specific
        place.
    AmenityPlaceDelete (Resource): Deletes a specific amenity from a place.
    ReviewPlaceUser (Resource): Adds a review for a place by a specific user.
    ReviewPlaceList (Resource): Retrieves all reviews associated with a specific
        place.
    AmenityReviewDelete (Resource): Deletes a specific review from a place.
    PlaceAmenityName (Resource): Retrieves all places that contain a specified
        amenity.

Attributes:
    places_bp (Blueprint): Flask blueprint for place routes.
    api (Namespace): Namespace for place-related API endpoints.
    place_model (model): Model schema for Place responses.
    place_creation_model (model): Model schema for creating a Place.
    get_amenities_model (model): Model schema for retrieving amenities.
    add_review_model (model): Model schema for creating a review for a place.
    get_all_reviews_success_model (model): Model schema for retrieving all
        reviews of a place.
"""

from flask import Blueprint, current_app, request, abort
from flask_restx import api, Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore

from app.api.v1.routes_reviews import review_model
from app.api.v1.routes_amenities import amenity_model, amenity_creation_model


places_bp = Blueprint('places', __name__)
api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'type': fields.String(required=False, description='Type will be given in response', example='place'),
    'id': fields.String(required=False, description='Id will be given in response', example=''),
    'title': fields.String(required=True, description='Name of the place', example='Chez Johnny'),
    'amenities': fields.List(fields.String, required=False, description='List of amenities', example=["BBQ", "Jacuzzi"]),
    'reviews': fields.List(fields.String, required=False, description='List of reviews', example=["e280c46e-3b28-424e-b864-737792145b70"]),
    'price': fields.Float(required=True, description='Price per night', example='150.50'),
    'description': fields.String(required=True, description='Description of the place', example='The rocker place'),
    'latitude': fields.Float(required=True, description='Latitude coordonates of the place', example='23.2356'),
    'longitude': fields.Float(required=True, description='Longitude coordinates of the place', example='54.4577'),
    'owner_first_name': fields.String(required=False, description='First_name of the owner of those places', example="Johnny"),
    'owner_id': fields.String(required=True, description='Id of the owner of the place', example='0defc403-97f3-4784-83c2-363dd7982c61'),
    'created_at': fields.String(required=False, description='Time of creation, given in response', example=''),
    'updated_at': fields.String(required=False, description='Time of update, given in response', example=''),
})

place_creation_model = api.model('Place_creation', {
    'title': fields.String(required=True, description='Name of the place', example='Chez Johnny'),
    'price': fields.Float(required=True, description='Price per night', example='150.50'),
    'description': fields.String(required=True, description='Description of the place', example='The rocker place'),
    'latitude': fields.Float(required=True, description='Latitude coordonates of the place', example='23.2356'),
    'longitude': fields.Float(required=True, description='Longitude coordinates of the place', example='54.4577'),
})

get_amenities_model = api.model('Get_amenities_model', {
    'place_id': fields.String(required=False, description='Id of the place to retrieve from', example=''),
    'place_amenities': fields.List(fields.String, required=False, description='List of amenities for a place', example=['Sauna'])
})

add_review_model = api.model('Add_review_model', {
    'text': fields.String(required=True, description='Text content for the new review', example='Great place for a relaxing time'),
    'rating': fields.Integer(required=True, description='Rating of the place, from 1 to 5', example='4'),
})

get_all_reviews_success_model = api.model('GetAllReviews', {
    'reviews': fields.List(fields.Nested(api.model('Review', {
        'id': fields.String(required=True, description='Unique identifier of the review', example='007c0cdd-c2d1-4232-b262-6314522aca45'),
        'place_name': fields.String(required=False, description='Name of the reviewed place', example='007c0cdd-c2d1-4232-b262-6314522aca45'),
        'user_id': fields.String(required=False, description='User_id of the reviewer', example='007c0cdd-c2d1-4232-b262-6314522aca45'),
        'user_first_name': fields.String(required=False, description='First_name of the reviewer', example='Johnny'),
        'text': fields.String(required=False, description='Content of the review', example='Very nice'),
        'rating': fields.Integer(required=False, description='Rating of the place from 1 to 5', example='4'),
    })), required=False, description='List of reviews for the place', example=[{}]),
})

auth_header = {'Authorization': {
        'description': 'Bearer <JWT Token>',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}

@api.route('/')
class PlaceList(Resource):
    """Resource for retrieving all places."""

    @api.doc('get_all_places')
    @api.marshal_list_with(place_model)
    def get(self):
        """
        Retrieves all places.

        Returns:
            JSON array of all places, with place attributes.
        """
        try:
            facade = current_app.extensions['HBNB_FACADE']

        
            places = facade.place_facade.get_all_places()

            if not places:
                raise ValueError(f"No place found")

            return places, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>


@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Resource for retrieving, updating, or deleting a specific place by ID."""

    @api.doc('get_place')
    @api.marshal_with(place_model)
    def get(self, place_id):
        """
        Retrieves a specific place by its ID.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            JSON object with the place's details.
        """
        try:
            facade = current_app.extensions['HBNB_FACADE']

            place = facade.place_facade.get_place(place_id)

            return place, 200

        except ValueError as e:
            abort(404, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

    @api.doc('update_place', params=auth_header)
    @api.expect(place_creation_model)
    @api.marshal_with(place_model)
    @jwt_required()
    def put(self, place_id):
        """
        Updates an existing place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            JSON object with the updated place's details.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']

            updated_data = request.get_json()

            place = facade.place_facade.get_place(place_id)
            if not place:
                raise ValueError('error: Place not found')

            if not is_admin and place["owner_id"] != current_user["id"]:
                raise ValueError('error: Unauthorized action, you must be the owner of the place to update it')

            updated_place = facade.place_facade.update_place(place_id, updated_data)

            return updated_place, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

    @api.doc('delete_place', params=auth_header)
    @jwt_required()
    def delete(self, place_id):
        """
        Deletes a place and its associated instances.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            Success message if deletion is successful.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            if not is_admin and place_id != current_user["id"]:
                raise ValueError('error: Unauthorized action, you can only modify your own data')

            facade_relation_manager.delete_place_and_associated_instances(place_id)

            return {f"Place: {place_id} has been deleted"}, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>


@api.route('/<string:place_id>/user')
@api.param('place_id')
class PlaceUserOwnerDetails(Resource):
    """Resource for deleting a place from both the place repository and the associated user repository. """

    @api.doc('delete_place_in_place_repo_and_user_repo', params=auth_header)
    @jwt_required()
    def delete(self, place_id):
        """
        Deletes a place from both the place repository and the associated user.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            Success message indicating the place was removed from both repositories.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            if not is_admin and place_id != current_user["id"]:
                raise ValueError('error: Unauthorized action, you can only modify your own data')

            place = facade.place_facade.get_place(place_id)
            user_id = place.get("owner_id")
            facade_relation_manager.delete_place_from_owner_place_list(place_id, user_id)

            return (f"Place: {place_id} has been deleted from user_place_list and place repo")

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>

@api.route('/<string:place_id>/amenities')
@api.param('place_id', 'The place identifier')
class AmenityPlaceList(Resource):
    """Resource for managing amenities associated with a specific place."""

    @api.doc('add_amenity_to_a_place', params=auth_header)
    @api.expect(amenity_creation_model)
    @api.marshal_with(amenity_model)  # type: ignore
    @jwt_required()
    def post(self, place_id):
        """
        Adds a new amenity to the specified place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            JSON representation of the newly added amenity.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            place = facade.place_facade.get_place(place_id)

            if not is_admin and place["owner_id"] != current_user["id"]:
                raise ValueError('error: Unauthorized action, you can only modify your own data')

            amenity_data = request.get_json()
            amenities = facade_relation_manager.add_amenity_to_a_place(place_id, amenity_data)

            return amenities, 201

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

    @api.doc('get_all_amenity_names_for_a_place')
    @api.marshal_with(get_amenities_model)  # type: ignore
    def get(self, place_id):
        """
        Retrieves all amenity names associated with a specific place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            JSON object with a list of amenity names.
        """
        try:
            facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            amenities = facade_relation_manager.get_all_amenities_names_from_place(place_id)

            amenities_response = {
                "place_id": place_id,
                "place_amenities": amenities
            }

            return amenities_response, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500


@api.route('/<string:place_id>/amenities/<string:amenity_name>')
@api.param('place_id', 'The place identifier')
@api.param('amenity_name', 'The amenity name to delete')
class AmenityPlaceDelete(Resource):
    """Resource for deleting a specific amenity from a place."""
    @api.doc('get_all_amenity_names_for_a_place', params=auth_header)
    @jwt_required()
    def delete(self, place_id, amenity_name):
        """
        Deletes a specific amenity from a place.

        Args:
            place_id (str): The unique identifier of the place.
            amenity_name (str): The name of the amenity to remove.

        Returns:
            Success message indicating the amenity was removed from the place.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            place = facade.place_facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            user_id = place["owner_id"]

            if not is_admin and user_id != current_user["id"]:
                raise ValueError('error: Unauthorized action, you can only update your own place')

            place = facade.place_facade.get_place(place_id)

        except ValueError as f:
            abort(400, str(f))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

        if amenity_name in place["amenities"]:
            try:
                facade_relation_manager.delete_amenity_from_place_list(
                    amenity_name, place_id)

                return {f"Amenity: {amenity_name} has been deleted from the place_amenities list"}, 200

            except ValueError as e:
                abort(400, str(e))

        else:
            return {"message": f"Amenity: {amenity_name} not found in the place_amenities list"}, 400

 #   <------------------------------------------------------------------------>


@api.route('/<string:place_id>/reviews/<string:user_id>')
@api.param('place_id', 'The place identifier')
@api.param('user_id', 'The reviewer identifier')
class ReviewPlaceUser(Resource):
    """Resource for adding a review to a place by a specific user."""

    @api.doc('add_review_to_a_place', params=auth_header)
    @api.expect(add_review_model)
    @api.marshal_with(review_model)  # type: ignore
    @jwt_required()
    def post(self, place_id, user_id):
        """
        Adds a review for a place by a specific user.

        Args:
            place_id (str): The unique identifier of the place.
            user_id (str): The unique identifier of the user submitting the review.

        Returns:
            JSON representation of the newly added review.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            place = facade.place_facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            reviews = facade.review_facade.get_all_reviews()
            for review in reviews:
                if not is_admin and review["user_id"] == current_user["id"] and review["place_id"] == place_id:
                    raise ValueError('error: Unauthorized action: You already reviewed this place.')

            if not is_admin and place["owner_id"] == user_id:
                raise ValueError('error: Unauthorized action, you can not review your own place')

            if not is_admin and user_id != current_user["id"] :
                raise ValueError('error: Unauthorized action, the user_id is incorect')
            
            new_review = request.get_json()

        
            review = facade_relation_manager.create_review_for_place(place_id, user_id, new_review)

            return review, 201

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>


@api.route('/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
@api.param('user_id', 'The reviewer identifier')
class ReviewPlaceList(Resource):
    """Resource for retrieving all reviews associated with a specific place."""

    @api.doc('get_all_reviews_for_a_place')
    @api.marshal_with(get_all_reviews_success_model)
    def get(self, place_id):
        """
        Retrieves all reviews associated with a specific place.

        Args:
            place_id (str): The unique identifier of the place.

        Returns:
            JSON object containing a list of reviews for the place.
        """
        try:
            facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            reviews_list = facade_relation_manager.get_all_reviews_dict_from_place_reviews_id_list(place_id)

            reviews_response = {
                "reviews": reviews_list
            }

            return reviews_response, 200

        except ValueError as e:
            abort(400, str(e))
        
        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>


@api.route('/<string:place_id>/review/<string:review_id>')
@api.param('place_id', 'The place identifier')
@api.param('review_id', 'The review to delete from the place')
class AmenityReviewDelete(Resource):
    """Resource for deleting a specific review from a place."""

    @api.doc('delete_a_review_from_a_place', params=auth_header)
    @jwt_required()
    def delete(self, place_id, review_id):
        """
        Deletes a specific review from a place.

        Args:
            place_id (str): The unique identifier of the place.
            review_id (str): The unique identifier of the review to delete.

        Returns:
            Success message indicating the review was removed from the place.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            place = facade.place_facade.get_place(place_id)
            if not place:
                raise ValueError('error: Place not found')
            
            user_id = place["owner_id"]

            if not is_admin and user_id != current_user["id"]:
                raise ValueError('error: Unauthorized action, you can only update your own place')

            facade_relation_manager.delete_review_from_place_list(review_id, place_id)

            return {"message": f"Review: {review_id} has been deleted from the place_reviews list"}, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>


@api.route('/amenity/<string:amenity_name>')
@api.param('amenity_name', 'The name of the amenity')
class PlaceAmenityName(Resource):
    """Resource for retrieving all places that contain a specified amenity."""

    @api.doc('get_all_places_with_specifique_amenity')
    @api.marshal_list_with(place_model)
    def get(self, amenity_name):
        """
        Retrieves all places that include a specified amenity.

        Args:
            amenity_name (str): The name of the amenity to filter places by.

        Returns:
            JSON array of places containing the specified amenity.
        """
        try:
            facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            amenities = facade_relation_manager.get_all_places_with_specifique_amenity(amenity_name)

            return amenities, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>
