"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from google.appengine.ext import ndb

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

class Greeting(ndb.Model):
	content = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World! gae!'

@app.route('/hi/<user>')
def hi(user):
	greeting = Greeting(parent=ndb.Key("Book",user),content=user)
	greeting.put()
	return 'hi ' + user + ' !!!'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

