#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template, abort
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Display a HTML page with a list of all State objects"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Display a HTML page with a State object and its Cities if found"""
    state = storage.get(State, id)
    if not state:
        return render_template('9-state_not_found.html'), 404

    cities = sorted(state.cities,
                    key=lambda city: city.name) if state.cities else []
    return render_template('9-state.html', state=state, cities=cities)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
