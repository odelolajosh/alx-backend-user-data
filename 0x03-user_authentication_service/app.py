#!/usr/bin/env python3
""" Authentication API. """
from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/", strict_slashes=True)
def status():
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
