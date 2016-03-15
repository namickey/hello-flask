from flask import Flask, redirect, url_for, render_template
from google.appengine.ext import ndb
import pytz

app = Flask(__name__)

class Sensor(ndb.Model):
    value = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_sensor(cls, ancestor_key):
        #.order(-Sensor.date)
        return cls.query(ancestor=ancestor_key)

@app.route('/<cate>')
def show(cate):
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    ancestor_key = ndb.Key("Sensor", cate)
    sensors = Sensor.query_sensor(ancestor_key)
    s = ''
    for sensor in sensors:
        s = s + '{x: \'' + str(tz_tokyo.fromutc(sensor.date)).split('.')[0] + '\', y: ' + sensor.value + '},'
    return render_template('index.html', data=s)

@app.route('/<cate>/<value>')
def regist(cate, value):
    sensor = Sensor(parent=ndb.Key("Sensor",cate),value=value)
    sensor.put()
    return redirect(url_for('show', cate=cate))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

