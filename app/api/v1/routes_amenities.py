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

amenity_creation_model = api.model('Amenity_creation', {
    'name': fields.String(required=True, description='Name of the amenity', example='Sauna'),
})

#   <------------------------------------------------------------------------>

@api.route('/')
class AmenityList(Resource):
    @api.doc('create_amenity')
    @api.expect(amenity_creation_model)
    @api.marshal_with(amenity_model, code=201) #type: ignore
    def post(self):
        """Create a new amenity"""
        facade = current_app.extensions['HBNB_FACADE']
        new_amenity = request.get_json()
        
        try:
            amenity = facade.amenity_facade.create_amenity(new_amenity)

            return amenity, 201

        except ValueError as e:
            abort(400, str(e))

    
    @api.doc('get_all_amenities')
    @api.marshal_with(amenity_model, code=201) #type: ignore
    def get(self):
        """Get a list of all amenities"""
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
    @api.doc('get_amenity')
    @api.marshal_with(amenity_model) # type: ignore
    def get(self, amenity_id):
        """Get an amenity by id"""
        facade = current_app.extensions['HBNB_FACADE']

        try:
            amenity = facade.amenity_facade.get_amenity(amenity_id)

            return amenity, 200

        except ValueError as e:
            abort(404, str(e))


    @api.doc('update_amenity')
    @api.expect(amenity_creation_model)
    @api.marshal_with(amenity_model) # type: ignore
    def put(self, amenity_id):
        """Update an amenity"""
        facade = current_app.extensions['HBNB_FACADE']
        updated_data = request.get_json()

        try:
            updated_amenity = facade.amenity_facade.update_amenity(amenity_id, updated_data)

            return updated_amenity, 200

        except ValueError as e:
            abort(404, str(e))
    
    @api.doc('delete_amenity')
    def delete(self, amenity_id):
        """Delete an amenity"""
        facade = current_app.extensions['HBNB_FACADE']

        try:
            facade.amenity_facade.delete_amenity(amenity_id)

            return (f"Amenity: {amenity_id} has been deleted."), 200

        except ValueError as e:
            abort(404, str(e))
