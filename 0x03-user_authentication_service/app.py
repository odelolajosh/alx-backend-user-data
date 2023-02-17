#!/usr/bin/env python3
""" Authentication API. """
from flask import Flask, jsonify, request, abort, redirect, Response
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
        abort(401)

    session_id = auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ DELETE /sessions
    Logs out a user.
    Return:
        - Message
        - 403 if no session cookie.
    """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    auth.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
