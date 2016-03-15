"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, redirect, url_for
from google.appengine.ext import ndb

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

class Sensor(ndb.Model):
    value = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_sensor(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)

@app.route('/tem')
def show():
    cate = 'tem'
    ancestor_key = ndb.Key("Sensor", cate)
    sensors = Sensor.query_sensor(ancestor_key).fetch(20)
    s = ''
    for sensor in sensors:
        s = s + sensor.value + ',' + str(sensor.date) + '\n'
    return 'Hello World! gae!\n' + s

@app.route('/<cate>/<value>')
def regist(cate, value):
    sensor = Sensor(parent=ndb.Key("Sensor",cate),value=value)
    sensor.put()
    return redirect(url_for('show') + "/" + cate)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

