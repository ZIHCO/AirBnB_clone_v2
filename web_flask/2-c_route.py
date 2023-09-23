#!/usr/bin/python3
"""starts a flask web application"""
from flask import Flask
from markupsafe import escape


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """Home page"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """hbnb page"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """dynamic route"""
    if "_" in text:
        text_list = text.split("_")
        text = " ".join(text_list)
    string = "C " + text
    return escape(string)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
