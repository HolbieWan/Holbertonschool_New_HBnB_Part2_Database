"""
routes_reviews.py

This module defines Flask routes for review-related operations, including 
creating, retrieving, updating, and deleting reviews.

Classes:
    ReviewList (Resource): Manages the creation of a new review and 
        retrieval of all reviews.
    ReviewResource (Resource): Handles retrieval, updating, and deletion of a 
        specific review by ID.

Attributes:
    reviews_bp (Blueprint): Flask blueprint for review routes.
    api (Namespace): Namespace for review-related API endpoints.
    review_model (model): Model schema for Review responses.
    review_creation_model (model): Model schema for creating a Review.
    review_update_model (model): Model schema for updating a Review.
"""

from flask import jsonify, abort, request, Blueprint, current_app
from flask_restx import api, Namespace, Resource, fields

reviews_bp = Blueprint('reviews', __name__)
api = Namespace('reviews', description='Reviews operations')

review_model = api.model('Review', {
    'type': fields.String(required=False, description='Type will be given in response', example='review'),
    'id': fields.String(required=False, description='Id will be given in response', example=''),
    'text': fields.String(required=True, description='Text of the review', example='Very nice !'),
    'rating': fields.Integer(required=True, description='Rating from the user for this place', example='4'),
    'place_id': fields.String(required=True, description='Id of the reviewed place', example='b8bf4d6f-7f4e-4201-ab6e-3b1287c40f46'),
    'place_name': fields.String(required=False, description='Name of the reviewed place', example='Chez Johnny'),
    'user_id': fields.String(required=True, description='Id of the owner of the place', example='007c0cdd-c2d1-4232-b262-6314522aca45'),
    'user_first_name': fields.String(required=False, description='First_name of the reviewer ', example='Johnny'),
    'created_at': fields.String(required=False, description='Time of creation, given in response', example=''),
    'updated_at': fields.String(required=False, description='Time of update, given in response', example=''),
})

review_creation_model = api.model('Review_creation', {
    'text': fields.String(required=True, description='Text of the review', example='Very nice !'),
    'rating': fields.Integer(required=True, description='Rating from the user for this place', example='4'),
    'place_id': fields.String(required=True, description='Id of the reviewed place', example='b8bf4d6f-7f4e-4201-ab6e-3b1287c40f46'),
    'place_name': fields.String(required=False, description='Name of the reviewed place', example='Chez Johnny'),
    'user_id': fields.String(required=True, description='Id of the owner of the place', example='007c0cdd-c2d1-4232-b262-6314522aca45'),
    'user_first_name': fields.String(required=False, description='First_name of the reviewer ', example='Johnny'),
})

review_update_model = api.model('Review_update', {
    'text': fields.String(required=True, description='Text of the review', example='Very nice !'),
    'rating': fields.Integer(required=True, description='Rating from the user for this place', example='4')
})


@api.route('/')
class ReviewList(Resource):
    """Resource for creating and listing all reviews."""
    
    @api.doc('create_review')
    @api.expect(review_creation_model)
    @api.marshal_with(review_model, code=201)  # type: ignore
    def post(self):
        """
        Creates a new review.

        Expects:
            JSON payload with review details.

        Returns:
            JSON representation of the created review.
        """
        facade = current_app.extensions['HBNB_FACADE']
        new_review_data = request.get_json()

        try:
            review = facade.review_facade.create_review(new_review_data)

            return review, 201

        except ValueError as e:
            abort(400, str(e))

    @api.doc('get_all_reviews')
    @api.marshal_with(review_model, code=201)  # type: ignore
    def get(self):
        """
        Retrieves all reviews.

        Returns:
            List of reviews.
        """
        facade = current_app.extensions['HBNB_FACADE']

        try:
            reviews = facade.review_facade.get_all_reviews()

            if not reviews:
                raise ValueError("No review found")

            return reviews, 200

        except ValueError as e:
            abort(400, str(e))

    #   <------------------------------------------------------------------------>


@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Resource for retrieving, updating, or deleting a review by ID."""

    @api.doc('get_a_review_by_id')
    @api.marshal_with(review_model)
    def get(self, review_id):
        """
        Retrieves a review by its unique identifier.

        Args:
            review_id (str): Unique identifier of the review.

        Returns:
            JSON representation of the review.
        """
        facade = current_app.extensions['HBNB_FACADE']

        try:
            review = facade.review_facade.get_review(review_id)

            return review, 200

        except ValueError as e:
            abort(400, str(e))

    @api.doc('update_review')
    @api.expect(review_update_model)
    @api.marshal_with(review_model)
    def put(self, review_id):
        """
        Updates an existing review.

        Args:
            review_id (str): Unique identifier of the review.

        Returns:
            JSON representation of the updated review.
        """
        facade = current_app.extensions['HBNB_FACADE']
        new_data = request.get_json()

        try:
            review = facade.review_facade.update_review(review_id, new_data)

            return review, 201

        except ValueError as e:
            abort(400, str(e))

    @api.doc('delete_review')
    def delete(self, review_id):
        """
        Deletes a review by its unique identifier.

        Args:
            review_id (str): Unique identifier of the review.

        Returns:
            Success message upon deletion.
        """
        facade = current_app.extensions['HBNB_FACADE']

        try:
            facade.review_facade.delete_review(review_id)

            return (f"Review: {review_id} has been deleted.")

        except ValueError as e:
            abort(400, str(e))
