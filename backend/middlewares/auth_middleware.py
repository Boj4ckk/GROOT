

from flask import request, jsonify
from functools import wraps
from Adapter.jwt_adapter import JwtAdapter



def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("access_token")  # <- ici on lit le cookie
        if not token:
            return jsonify({"erreur": "Unauthorized"}), 401
        try:
            payload = JwtAdapter.decode(token)
            request.user_id = payload["user_id"]
        except Exception:
            return jsonify({"erreur": "Invalid or expired token"}), 401
        return f(*args, **kwargs)
    return decorated

           