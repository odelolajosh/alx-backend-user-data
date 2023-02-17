#!/usr/bin/env python3
""" Authentication API. """
from flask import Flask, jsonify, request, abort, Response
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
    Register a user.
    Return:
        - Email of the user.
        - 400 if email already registered.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = auth.register_user(email, password)
        if not user:
            return jsonify({"message": "user not created"}), 400
        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ POST /sessions
    Logs in a user.
    Return:
        - Email of the user.
        - Message
        - 400 if email already registered.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not auth.valid_login(email, password):
        return abort(401)

    auth.create_session(email)
    return jsonify({"email": email, "message": "logged in"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
