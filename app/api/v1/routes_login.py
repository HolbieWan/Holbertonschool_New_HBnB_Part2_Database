"""
routes_login.py

This module defines a Flask route for user authentication, allowing users to
log in and receive a JSON Web Token (JWT) for authorization in protected
endpoints.

Classes:
    Login (Resource): Handles user authentication by verifying credentials
        and issuing a JWT token upon successful login.

Attributes:
    login_bp (Blueprint): Flask blueprint for authentication routes.
    api (Namespace): Namespace for authentication-related API endpoints.
    login_model (model): Model schema for login request payload, requiring
        email and password fields.

Models:
    login_model (model): API model representing login attributes, specifically
        email and password, required for user authentication.
"""

from flask import Blueprint, current_app, request, abort
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token  # type: ignore


login_bp = Blueprint('login', __name__)
api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email', example="johnny.rocker@gmail.com"),
    'password': fields.String(required=True, description='User password', example="mypassword")
})


@api.route('/login')
class Login(Resource):
    """Resource for authenticating users and generating a JWT token for authorization."""

    @api.expect(login_model)
    def post(self):
        """
        Authenticates a user based on provided email and password.

        Expects:
            JSON payload containing `email` and `password` fields.

        Returns:
            dict: JSON response containing the JWT `access_token` if
            authentication is successful.

        Raises:
            ValueError: If credentials are invalid or user is not found.
            HTTP 400: If any error occurs during authentication.
        """
        facade = current_app.extensions['HBNB_FACADE']
        credentials = request.get_json()

        try:
            user = facade.user_facade.get_user_by_email(credentials["email"])

            for user in user:
                if not user or not user.verify_password(
                        credentials["password"]):
                    raise ValueError("Error: invalid credentials")

            access_token = create_access_token(
                identity={'id': str(user.id), 'is_admin': user.is_admin})

        except ValueError as e:
            abort(400, str(e))

        return {'access_token': access_token}, 200
