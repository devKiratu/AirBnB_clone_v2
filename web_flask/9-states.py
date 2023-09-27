#!/usr/bin/python3
"""This script starts a Flask web app"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states", strict_slashes=False)
@app.route("/states/<id>", strict_slashes=False)
def show_states(id=None):
    """lists all states via the /states route and a single
    state via /states/<id>"""
    states = storage.all(State)
    found = False
    state_by_id = None
    for state in states.values():
        if state.id == id:
            found = True
            state_by_id = state
            break
    return render_template('9-states.html',
                           id=id,
                           states=states,
                           found=found,
                           state_by_id=state_by_id)


@app.teardown_appcontext
def tear_down(exception):
    """removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
