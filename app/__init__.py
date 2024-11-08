"""
Main application initialization module.

This module contains the `create_app` function, which initializes the Flask
application, sets up configurations, extensions, blueprints, and namespaces
for API endpoints.
"""

import os

from flask import Flask
from flask_restx import Api

from config import config
from app.extensions import bcrypt, jwt, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.api.v1.routes_users import users_bp
from app.api.v1.routes_places import places_bp
from app.api.v1.routes_amenities import amenities_bp
from app.api.v1.routes_reviews import reviews_bp
from app.api.v1.routes_login import login_bp
from app.api.v1.routes_users import api as users_ns
from app.api.v1.routes_places import api as places_ns
from app.api.v1.routes_amenities import api as amenities_ns
from app.api.v1.routes_reviews import api as reviews_ns
from app.api.v1.routes_login import api as login_ns
from app.services.facade import HBnBFacade
from app.services.facade_user import UserFacade
from app.services.facade_place import PlaceFacade
from app.services.facade_amenity import AmenityFacade
from app.services.facade_review import ReviewFacade
from app.services.facade_relations_manager import FacadeRelationManager
from app.services.sqlalchemy_facade_relation_manager import SQLAlchemyFacadeRelationManager
from app.persistence.repo_selector import RepoSelector


def create_app(config_name='default'):
    """
    Initialize and configure the Flask application.

    Args:
        config_name (str): The configuration name to be used
        (e.g., 'development').

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Initialize repositories
    repo_type = app.config.get('REPO_TYPE', 'in_memory')
    user_repo_selector = RepoSelector(repo_type, "user_data.json")
    place_repo_selector = RepoSelector(repo_type, "place_data.json")
    amenity_repo_selector = RepoSelector(repo_type, "amenity_data.json")
    review_repo_selector = RepoSelector(repo_type, "review_data.json")

    # Check if using a database repository and pass the models
    if repo_type == 'in_DB':
        user_repo = user_repo_selector.select_repo(User)
        place_repo = place_repo_selector.select_repo(Place)
        amenity_repo = amenity_repo_selector.select_repo(Amenity)
        review_repo = review_repo_selector.select_repo(Review)
    else:
        # For in-memory or file repositories, no need to pass the model
        user_repo = user_repo_selector.select_repo()
        place_repo = place_repo_selector.select_repo()
        amenity_repo = amenity_repo_selector.select_repo()
        review_repo = review_repo_selector.select_repo()

    # Initialize facades
    user_facade = UserFacade(user_repo)
    place_facade = PlaceFacade(place_repo)
    review_facade = ReviewFacade(review_repo)
    amenity_facade = AmenityFacade(amenity_repo)

    # Initialize Facade with existing facades
    hbnb_facade = HBnBFacade(user_facade, place_facade, amenity_facade, review_facade)
    facade_relation_manager = FacadeRelationManager(user_facade, place_facade, amenity_facade, review_facade)
    sqlalchemy_facade_relation_manager = SQLAlchemyFacadeRelationManager(user_facade, place_facade, amenity_facade, review_facade)

    # Store hbnb_facade and other facades in app.extensions
    app.extensions['HBNB_FACADE'] = hbnb_facade
    app.extensions['FACADE_RELATION_MANAGER'] = facade_relation_manager
    app.extensions['SQLALCHEMY_FACADE_RELATION_MANAGER'] = (sqlalchemy_facade_relation_manager)

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(amenities_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(login_bp)

    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(login_ns, path='/api/v1/login')

    print(f"Starting the app with config: {config_name}")
    print(f"Starting the app with storage: {repo_type}")

    return app
