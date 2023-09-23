#!/usr/bin/python3
"""starts a flask web application"""
from flask import Flask
from flask import render_template
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


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
def python_route(text="is cool"):
    """dynamic route"""
    if "_" in text:
        text_list = text.split("_")
        text = " ".join(text_list)
    string = "Python " + text
    return escape(string)


@app.route("/number/<int:text>", strict_slashes=False)
def number_route(text):
    """dynamic route"""
    return "{} is a number".format(text)


@app.route("/number_template/<int:text>", strict_slashes=False)
def number_template(text):
    """render html"""
    return render_template("5-number.html", name=text)


@app.route("/number_odd_or_even/<int:text>", strict_slashes=False)
def number_odd_or_even(text):
    """render html"""
    if text % 2 == 0:
        int_type = "even"
    else:
        int_type = "odd"
    return render_template("6-number_odd_or_even.html", name=[text, int_type])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
