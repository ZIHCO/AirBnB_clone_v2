#!/usr/bin/python3
"""script starts a flask web app"""
from flask import Flask
from models import storage
from models.state import State
from flask import render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown():
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
