#!/usr/bin/python3
""" Create a flask view for Amenities objects that
    handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def amenities_views():
    """ Retrieves all Amenity objects and returns a JSON response """
    amenities_list = []
    for value in storage.all(Amenity).values():
        amenities_list.append(value.to_dict())
    return (jsonify(amenities_list))


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenities_id_views(amenity_id):
    """ Retrieves a specific Amenity object by its
        amenity_id and returns a JSON response """
    get_id = storage.get(Amenity, amenity_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes a specific Amenity object by its amenity_id
        and returns an empty JSON response with the status
        code 200."""
    get_id = storage.get(Amenity, amenity_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Creates a new Amenity object based on the JSON data provided """
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "name" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    new_amenity_obj = Amenity(**data_req)
    new_amenity_obj.save()
    return (jsonify(new_amenity_obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates a specific Amenity object by its amenity_id """
    get_id = storage.get(Amenity, amenity_id)
    if get_id is None:
        abort(404)
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for key, value in data_req.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            setattr(get_id, key, value)
    get_id.save()

    return (jsonify(get_id.to_dict()), 200)
