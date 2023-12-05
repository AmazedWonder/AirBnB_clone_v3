#!/usr/bin/python3
""" Create a new view for State objects that
    handles all default RESTFul API actions """
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def states_views():
    """ Retrieves all State objects and returns a JSON
        response containing a list of state objects
   """
    list_states = []
    for value in storage.all(State).values():
        list_states.append(value.to_dict())
    return (jsonify(list_states))


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def states_id_views(state_id):
    """ Retrieves a specific State object by its state_id
        and returns a JSON response containing the state object
    """
    get_id = storage.get(State, state_id)
    if get_id is None:
        abort(404)
    return (jsonify(get_id.to_dict()))


@app_views.route('/states/<state_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a specific State object by its state_id
        and returns an empty JSON response with the status code 200.
    """
    get_id = storage.get(State, state_id)
    if get_id is None:
        abort(404)
    storage.delete(get_id)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a new State object based on the JSON
        data provided in the request body
    """
    data_req = request.get_json()
    if not data_req:
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if "name" not in data_req.keys():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    new_state_obj = State(**data_req)
    new_state_obj.save()
    return (jsonify(new_state_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ Updates a specific State object by its state_id
        based on the JSON data provided in the request body
    """
    get_id = storage.get(State, state_id)
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