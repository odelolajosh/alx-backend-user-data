#!/usr/bin/env python3
""" Authentication API. """
from flask import Flask, jsonify, request, Response
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=["GET"], strict_slashes=False)
def welcome() -> Response:
    """ Welcome message. """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> Response:
    """ POST /users
    Return:
      - User object JSON represented
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = auth.register_user(email, password)
        if not user:
            return jsonify({"message": "user not created"})
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
