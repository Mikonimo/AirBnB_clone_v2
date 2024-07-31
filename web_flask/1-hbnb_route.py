#!/usr/bin/python3
"""Starts a flask web application"""
from flask import Flask


app = Flask(__nam__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Prints HBNB"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def d_hbnb():
    """Prints HBNB"""
    return "HBNB"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
