"""
routes_users.py

This module defines Flask routes for user-related operations, including user
creation, updating, deletion, and retrieval. It also manages associated user
resources, such as places and reviews, through endpoints to create and
retrieve these related entities.

Classes:
    Home (Resource): A protected endpoint welcoming a logged-in user.
    UserList (Resource): Manages the creation and listing of users.
    UserResource (Resource): Manages retrieval, updating, and deletion of a
        specific user by ID.
    UserPlaceDetails (Resource): Manages creation and retrieval of places
        associated with a specific user.
    UserReviewDetails (Resource): Retrieves reviews associated with a user.

Attributes:
    users_bp (Blueprint): Flask blueprint for user routes.
    api (Namespace): Namespace for user-related API endpoints.
    user_model (model): Model schema for User responses.
    user_creation_model (model): Model schema for creating a User.
    user_update_model (model): Model schema for updating a User.
    get_all_places_success_model (model): Model schema for listing places.

Models:
    auth_header (dict): Authorization header specification for JWT.
    user_model (model): API model representing user attributes.
    user_creation_model (model): API model for user creation payload.
    user_update_model (model): API model for updating a user's details.
    get_all_places_success_model (model): API model for listing user's places.
"""

from flask import Blueprint, current_app, request, abort
from flask_restx import Api, Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity # type: ignore
from email_validator import EmailNotValidError

from app.api.v1.routes_places import place_model, place_creation_model
from app.api.v1.routes_reviews import review_model
from app.extensions import bcrypt


users_bp = Blueprint('users', __name__)
api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'type': fields.String(required=False, description='Type will be given in response', example='user'),
    'id': fields.String(required=False, description='id given in the response', example=''),
    'first_name': fields.String(required=True, description='First name', example='Johnny'),
    'last_name': fields.String(required=True, description='Last name', example='Rocker'),
    'email': fields.String(required=True, description='Email address', example='johnny.rocker@gmail.com'),
    'password' : fields.String(required=True, description="Password", example='mypassword'),
    'is_admin': fields.Boolean(required=True, description='Admin rights', example='false'),
    'places': fields.List(fields.String, required=False, description='List of places for this user', example=[]),
    'created_at': fields.String(required=False, description='Time of creation, given in response', example=''),
    'updated_at': fields.String(required=False, description='Time of update, given in response', example=''),
})

user_creation_model = api.model('User_creation', {
    'first_name': fields.String(required=True, description='First name', example='Johnny'),
    'last_name': fields.String(required=True, description='Last name', example='Rocker'),
    'email': fields.String(required=True, description='Email address', example='johnny.rocker@gmail.com'),
    'password' : fields.String(required=True, description="Password", example='mypassword'),
    # 'is_admin': fields.Boolean(required=True, description='Admin rights', example='false'),
})

user_update_model = api.model('User_update', {
    'first_name': fields.String(required=True, description='First name', example='Johnny'),
    'last_name': fields.String(required=True, description='Last name', example='Rocker'),
    'email': fields.String(required=True, description='Email address', example='johnny.rocker@gmail.com'),
    'password': fields.String(required=False, description='Password', example='mypassword')
})

get_all_places_success_model = api.model('GetAllPlaces', {
    'places': fields.List(fields.Nested(api.model('Place', {
    'id': fields.String(required=True, description='Unique identifier of the place', example='0defc403-97f3-4784-83c2-363dd7982c61'),
    'title': fields.String(required=True, description='Name of the place', example='Chez Johnny'),
    'amenities': fields.List(fields.String, required=False, description='List of amenities', example=["BBQ", "Jacuzzi"]),
    'reviews': fields.List(fields.String, required=False, description='List of reviews', example=[""]),
    'price': fields.Float(required=True, description='Price per night', example='150.50'),
    'description': fields.String(required=True, description='Description of the place', example='The rocker place'),
    'latitude': fields.Float(required=True, description='Latitude coordonates of the place', example='23.2356'),
    'longitude': fields.Float(required=True, description='Longitude coordinates of the place', example='54.4577'),
    'owner_first_name': fields.String(required=False, description='First_name of the owner of those places', example="Johnny"),
    'owner_id': fields.String(required=True, description='Id of the owner of the place', example='0defc403-97f3-4784-83c2-363dd7982c61'),
    'created_at': fields.String(required=True, description='Time of creation, given in response', example=''),
    'updated_at': fields.String(required=True, description='Time of update, given in response', example=''),
})), required=False, description='List of reviews for the place', example=[{}]),
})

auth_header = {'Authorization': {
        'description': 'Bearer <JWT Token>',
        'in': 'header',
        'type': 'string',
        'required': True
    }
}

@api.route('/home')
class Home(Resource):
    """A protected endpoint that welcomes a logged-in user."""

    @api.doc('home', params=auth_header)
    @jwt_required()
    def get(self):
        """Returns a personalized welcome message for the logged-in user."""
        facade = current_app.extensions['HBNB_FACADE']

        current_user = get_jwt_identity()
        current_user_id = current_user["id"]
        current_user = facade.user_facade.get_user(current_user_id)
        current_user_first_name = current_user["first_name"]
        current_user_last_name = current_user["last_name"]

        return {"message": f"Hello {current_user_first_name} {current_user_last_name}"}, 200
    
 #   <------------------------------------------------------------------------>

@api.route('/')
class UserList(Resource):
    """Resource for creating a new user and listing all users."""

    @api.doc('create_user', params=auth_header)
    @api.expect(user_creation_model)
    @api.marshal_with(user_model, code=201) # type: ignore
    @jwt_required()
    def post(self):
        """
        Creates a new user.

        Expects:
            JSON payload with user details, excluding `is_admin`.

        Returns:
            JSON representation of the created user with password masked.
        """
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403
            
            facade = current_app.extensions['HBNB_FACADE']
            user_data = request.get_json()

            new_user = facade.user_facade.create_user(user_data)
            new_user["password"] = "****"

            return new_user, 201

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500
    

    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """
        Retrieves all users in the system.

        Returns:
            List of user dictionaries with masked passwords.
        """
        try:
            facade = current_app.extensions['HBNB_FACADE']

            users = facade.user_facade.get_all_users()

            if not users:
                raise ValueError("No user found")
        
            for user in users:
                user["password"] = "****"

            return users, 200

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>

@api.route('/<string:user_id>')
@api.param('user_id', 'The User identifier')
class UserResource(Resource):
    """Resource for retrieving, updating, or deleting a specific user by ID."""

    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            JSON representation of the user with password masked.
        """
        try:
            facade = current_app.extensions['HBNB_FACADE']

            user = facade.user_facade.get_user(user_id)
            user["password"] = "****"

            return user, 200
        
        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500


    @api.doc('update_user', params=auth_header)
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    @jwt_required()
    def put(self, user_id):
        """
        Updates an existing user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            JSON representation of the updated user with masked password.
        """
        try:
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)
            facade = current_app.extensions['HBNB_FACADE']

            user = facade.user_facade.get_user(user_id)
            if not user:
                raise ValueError('error: User not found')

            if not is_admin and user["id"] != current_user["id"]:
                raise ValueError(f'error: Unauthorized action, you can only modify your own data')

            updated_data = request.get_json()

            new_password = updated_data["password"]
            new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            updated_data["password"] = new_password

            if not is_admin:
                updated_data["password"] = user["password"]

            updated_user = facade.user_facade.update_user(user_id, updated_data)
            updated_user["password"] = "****"

            return updated_user, 200
        
        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500


    # @api.doc('delete_user')
    # def delete(self, user_id):
    #     """Delete a user"""
    #     facade = current_app.extensions['HBNB_FACADE']

    #     try:
    #         facade.user_facade.delete_user(user_id)
    #         return {"message": f"User: {user_id} has been deleted"}, 200
        
    #     except ValueError as e:
    #         abort(400, str(e))


    @api.doc('delete_user', params=auth_header)
    @jwt_required()
    def delete(self, user_id):
        """
        Deletes a user along with all associated instances.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            Success message if deletion is successful.
        """
        try:
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')
            current_user = get_jwt_identity()
            is_admin = current_user.get('is_admin', False)

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            if not is_admin and user_id != current_user["id"]:
                raise ValueError('error: Unauthorized action, you can only modify your own data')
        
            facade_relation_manager.delete_user_and_associated_instances(user_id)
            return {"message": f"User: {user_id} has been deleted"}, 200
        
        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500

 #   <------------------------------------------------------------------------>

@api.route('/<string:user_id>/place')
@api.param('user_id', 'The User identifier')
class UserPlaceDetails(Resource):
    """Resource for creating a place for a user or retrieving places by user."""
    
    @api.doc('create_place', params=auth_header)
    @api.expect(place_creation_model)
    @api.marshal_with(place_model, code=201) # type: ignore
    @jwt_required()
    def post(self, user_id):
        """
        Creates a new place associated with a user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            JSON representation of the created place.
        """
        try:
            current_user = get_jwt_identity()
            repo_type = current_app.config.get('REPO_TYPE', 'in_memory')

            if repo_type == 'in_DB':
                facade_relation_manager = current_app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER']
            else:
                facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

        
            new_place_data = request.get_json()

            if user_id != current_user["id"]:
                raise ValueError('error: Unauthorized action, can only create place if you are the owner')

            new_place_data["amenities"] = []
            new_place_data["reviews"] = []

            place = facade_relation_manager.create_place_for_user(user_id, new_place_data)

            return place, 201

        except ValueError as e:
            abort(400, str(e))

        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500


    @api.doc('get_places_by_user_id')
    @api.marshal_with(get_all_places_success_model, code=200) # type: ignore
    def get(self, user_id):
        """
        Retrieves all places associated with a user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            List of places associated with the user.
        """
        try:
            facade = current_app.extensions['HBNB_FACADE']

            places = facade.place_facade.get_all_places_from_owner_id(user_id)

            places_response = {
                "places": places
            }

            return places_response, 200

        except ValueError as e:
            abort(400, str(e))
        
        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500
    
 #   <------------------------------------------------------------------------>

@api.route('/<string:user_id>/reviews')
@api.param('user_id', 'The User identifier')
class UserReviewDetails(Resource):
    """Resource for retrieving all reviews associated with a specific user."""
    @api.doc('Get_all_reviews_from_a_user')
    @api.marshal_with(review_model, code=201) # type: ignore
    def get(self, user_id):
        """
        Retrieves all reviews associated with a user.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            List of reviews for the specified user.
        """
        try:
            facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

            reviews = facade_relation_manager.get_all_reviews_from_user(user_id)
            
            return reviews, 201

        except ValueError as e:
            abort(400, str(e))
        
        except Exception as e:
            return {'error': 'An unexpected error occurred', 'details': str(e)}, 500