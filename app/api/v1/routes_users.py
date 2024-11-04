# routes_users.py

from flask import Blueprint, current_app, request, abort
from flask_restx import Api, Namespace, Resource, fields
from email_validator import EmailNotValidError

from app.api.v1.routes_places import place_model, place_creation_model
from app.api.v1.routes_reviews import review_model


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
    'is_admin': fields.Boolean(required=True, description='Admin rights', example='false'),
})

user_update_model = api.model('User_update', {
    'first_name': fields.String(required=True, description='First name', example='Johnny'),
    'last_name': fields.String(required=True, description='Last name', example='Rocker'),
    'email': fields.String(required=True, description='Email address', example='johnny.rocker@gmail.com'),
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


# @api.route('/home')
# class Home(Resource):
#     def get(self):
#         return "Welcome to the homepage"
    
 #   <------------------------------------------------------------------------>

@api.route('/')
class UserList(Resource):
    @api.doc('create_user')
    @api.expect(user_creation_model)
    @api.marshal_with(user_model, code=201) # type: ignore
    def post(self):
        """Create a new user"""
        facade = current_app.extensions['HBNB_FACADE']
        user_data = request.get_json()

        try:
            new_user = facade.user_facade.create_user(user_data)

            user_response = {
            "type": new_user["type"],
            "id": new_user["id"],
            "first_name": new_user["first_name"],
            "last_name": new_user["last_name"],
            "email": new_user["email"],
            "password": "****",
            "is_admin": new_user["is_admin"],
            "places" : [""],
            "created_at": "",
            "updated_at": ""
            }
            return user_response, 201

        except ValueError as e:
            abort(400, str(e))
    

    @api.doc('list_users')
    @api.marshal_list_with(user_model)
    def get(self):
        """Get all users"""
        facade = current_app.extensions['HBNB_FACADE']

        try:
            users = facade.user_facade.get_all_users()
            if not users:
                raise ValueError("No user found")
            return users, 200

        except ValueError as e:
            abort(400, str(e))

 #   <------------------------------------------------------------------------>

@api.route('/<string:user_id>')
@api.param('user_id', 'The User identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        facade = current_app.extensions['HBNB_FACADE']

        try:
            user = facade.user_facade.get_user(user_id)
            return user, 200
        
        except ValueError as e:
            abort(400, str(e))


    @api.doc('update_user')
    @api.expect(user_update_model)
    @api.marshal_with(user_model)
    def put(self, user_id):
        """Update a user"""
        facade = current_app.extensions['HBNB_FACADE']
        updated_data = request.get_json()

        try:
            updated_user = facade.user_facade.update_user(user_id, updated_data)
            return updated_user, 200
        
        except ValueError as e:
            abort(400, str(e))


    # @api.doc('delete_user')
    # def delete(self, user_id):
    #     """Delete a user"""
    #     facade = current_app.extensions['HBNB_FACADE']

    #     try:
    #         facade.user_facade.delete_user(user_id)
    #         return {"message": f"User: {user_id} has been deleted"}, 200
        
    #     except ValueError as e:
    #         abort(400, str(e))


    @api.doc('delete_user')
    def delete(self, user_id):
        """Delete a user and associated instances"""
        facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

        try:
            facade_relation_manager.delete_user_and_associated_instances(user_id)
            return {"message": f"User: {user_id} has been deleted"}, 200
        
        except ValueError as e:
            abort(400, str(e))

 #   <------------------------------------------------------------------------>

@api.route('/<string:user_id>/place')
@api.param('user_id', 'The User identifier')
class UserPlaceDetails(Resource):
    @api.doc('create_place')
    @api.expect(place_creation_model)
    @api.marshal_with(place_model, code=201) # type: ignore
    def post(self, user_id):
        """Create a new place for a user"""
        facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']
        new_place_data = request.get_json()

        new_place_data["amenities"] = []
        new_place_data["reviews"] = []

        try:
            place = facade_relation_manager.create_place_for_user(user_id, new_place_data)
            return place, 201

        except ValueError as e:
            abort(400, str(e))


    @api.doc('get_places_by_user_id')
    @api.marshal_with(get_all_places_success_model, code=200) # type: ignore
    def get(self, user_id):
        """Get all places from the user_id"""
        facade = current_app.extensions['HBNB_FACADE']

        try:
            places = facade.place_facade.get_all_places_from_owner_id(user_id)
            places_response = {
                "places": places
            }

        except ValueError as e:
            abort(400, str(e))
        
        return places_response, 200
    
 #   <------------------------------------------------------------------------>

@api.route('/<string:user_id>/reviews')
@api.param('user_id', 'The User identifier')
class UserReviewDetails(Resource):
    @api.doc('Get_all_reviews_from_a_user')
    @api.marshal_with(review_model, code=201) # type: ignore
    def get(self, user_id):
        """Get all reviews from a user """
        facade_relation_manager = current_app.extensions['FACADE_RELATION_MANAGER']

        try:
            reviews = facade_relation_manager.get_all_reviews_from_user(user_id)
            return reviews, 201

        except ValueError as e:
            abort(400, str(e))