#!/usr/bin/python3
""" Create a flask view for Users objects that
    handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def users_views():
    """ Retrieves all User objects and returns a JSON response """
    users_list = []
    for value in storage.all(User).values():
        users_list.append(value.to_dict())
    return (jsonify(users_list))


@app_views.route('/users/<user_id>', methods=["GET"], strict_slashes=False)
def users_id_views(user_id):
    """ Retrieves a specific User object by its
        amenity_id and returns a JSON response """
    get_id = storage.get(User, user_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/users/<user_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a specific User object by its amenity_id
        and returns an empty JSON response with the status
        code 200. """
    get_id = storage.get(User, user_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a new User object based on the JSON data provided """
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "email" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing email'}), 400))
    if "password" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing password'}), 400))
    new_user_obj = User(**data_req)
    new_user_obj.save()
    return (jsonify(new_user_obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Updates a specific User object by its amenity_id """
    get_id = storage.get(User, user_id)
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