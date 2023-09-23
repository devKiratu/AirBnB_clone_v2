#!/usr/bin/python3
"""
This script starts a Flask web application listening on 0.0.0.0:5000 and
serves two routes: '/' and '/hbnb'
"""

from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_HBNB():
    """displays 'hello HBNB!' on route /"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """displays 'HBNB' on route '/hbnb'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def hello_c(text):
    """prints a message about C that is contained in <text>"""
    msg = "C {}".format(text.replace('_', ' '))
    return msg


if __name__ == "__main__":
    app.run(host='0.0.0.0')
