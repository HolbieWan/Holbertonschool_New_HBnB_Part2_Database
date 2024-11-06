from flask import Blueprint, current_app, request, abort
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token # type: ignore

login_bp = Blueprint('login', __name__)
api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email', example="johnny.rocker@gmail.com"),
    'password': fields.String(required=True, description='User password', example="mypassword")
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        facade = current_app.extensions['HBNB_FACADE']
        credentials = request.get_json()

        try:
            user = facade.user_facade.get_user_by_email(credentials["email"])

            for user in user:
                if not user or not user.verify_password(credentials["password"]):
                    raise ValueError("Error: invalid credentials")

            access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        except ValueError as e:
            abort(400, str(e))
        
        return {'access_token': access_token}, 200

