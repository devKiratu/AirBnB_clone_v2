#!/usr/bin/python3
"""
This script starts a Flask web app listening on 0.0.0.0:5000 that displays
a html page with a lists of states in route /states_list
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """removes the current SQL Alchemy session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def show_states():
    """renders a html page with states from storage"""
    states = storage.all(State)
    formatted_states = []
    for state in states.values():
        formatted_states.append({'id': state.id, 'name': state.name})
    return render_template('7-states_list.html', states=formatted_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0')