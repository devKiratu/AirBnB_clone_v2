#!/usr/bin/python3
"""This script starts a flask web app"""

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def get_cities_by_states():
    """renders a template with cities ordered by state"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def tear_down(exception):
    """removes current SQL Alchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
