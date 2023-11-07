#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
It is connected to a database (via SQLAlchemy) and
has API access to retrieve and store data
"""
from flask import Flask, render_template, url_for
from models import storage
import uuid

# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exc):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    This prevents the following request from using the same session
    """
    storage.close()


@app.route('/3-hbnb/')
def hbnb_load_data(query_id=None):
    """
    handles request to custom template with states, cities & amentities
    This method is linked to /0-hbnb/ in the routes
    Data must be loaded from storage for rendering
    """
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amenities = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
                 for user in storage.all('User').values())
    cache_id = (str(uuid.uuid4()))

    context = {
        'states': states,
        'amenities': amenities,
        'places': places,
        'users': users,
        'cache_id': cache_id
    }
    return render_template('3-hbnb.html', **context)


if __name__ == "__main__":
    """MAIN Flask App at port 5000"""
    app.run(host=host, port=port)
