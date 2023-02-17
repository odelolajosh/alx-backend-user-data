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


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> Response:
    """ GET /profile
    Returns the user's profile.
    Return:
        - Email of the user.
        - 403 if no session cookie.
    """
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> Response:
    """ POST /reset_password
    Returns a reset password token.
    Return:
        - Email of the user.
        - 403 if no session cookie.
    """
    email = request.form.get("email")
    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> Response:
    """ PUT /reset_password
    Updates the user's password.
    Return:
        - Email of the user.
        - 403 if no session cookie.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
