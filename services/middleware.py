from functools import wraps
from flask import request, jsonify
from models import APIClient

def authenticate_client(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_id = request.headers.get("client_id")
        client_secret = request.headers.get("client_secret")

        if not client_id or not client_secret:
            return jsonify({"message": "Missing client credentials"}), 401

        client = APIClient.query.get(client_id)
        if not client or not client.is_active or not client.check_secret(client_secret):
            return jsonify({"message": "Invalid client credentials"}), 403

        return f(*args, **kwargs)
    
    return decorated_function
