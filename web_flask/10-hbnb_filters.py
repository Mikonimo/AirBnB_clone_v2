#!/usr/bin/python3
"""Starts a web flask application"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Remove the SQLAlchemy session after each request."""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display the HTML page with filters."""
    states = sorted(storage.all('State').values(), key=lambda x: x.name)
    amenities = sorted(storage.all('Amenity').values(), key=lambda x: x.name)

    # For DBStorage, use `cities` relationship
    # For FileStorage, use `cities` public getter method
    cities = []
    if storage.__class__.__name__ == 'DBStorage':
        for state in states:
            cities.extend(state.cities)
        cities = sorted(cities, key=lambda x: x.name)
    else:
        for state in states:
            cities.extend(state.cities)
        cities = sorted(cities, key=lambda x: x.name)

    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities, cities=cities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
