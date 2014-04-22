

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


DEFAULT_LOCATION_NAME = 'default_location'
DEFAULT_NAME = 'default_name'


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def location_key(location_name=DEFAULT_LOCATION_NAME):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Location', location_name)


class Location(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    name = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    votes = ndb.IntegerPropery(indexed=True)



class MainPage(webapp2.RequestHandler):

    def get(self):
        location_name = self.request.get('location_name',
                                          DEFAULT_LOCATION_NAME)
        greetings_query = Location.query(
            ancestor=location_key(location_name)).order(-Location.vote)
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'location_name': urllib.quote_plus(location_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))



class Location (webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        location_name = self.request.get('location_name',
                                          DEFAULT_LOCATION_NAME)
        greeting = Location(parent=location_key(location_name))

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.name = self.request.get('name')
        greeting.put()

        query_params = {'location_name': location_name}
        self.redirect('/?' + urllib.urlencode(query_params))

class VoteUp (webapp2.RequestHandler):

    def post(self):
	region_name = self.request.get('location_name',DEFAULT_LOCATION_NAME)
	location_query = Location.query(
	   ancestor=location_key(region_name))
	location_name = self.reguest.get('up')
	location_curr = location_query.filter(name=location_name)
	#add +1 to votes:
	location_curr.votes = location_curr.votes +1
	#update datastore
	location_curr.put()
	

class VoteDown (webapp2.RequestHandler):

    def post(self)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Location),
    ('/voteup', VoteUp),
], debug=True)
