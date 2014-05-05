from google.appengine.ext import ndb

isloggedin = False

def is_logged_in():
	return isloggedin

def create_login_url(string):
	return '/login'

def create_logout_url(string):
	return '/logout'

def get_current_user():
	return 'usertest'

def set_loggedin():
	isloggedin = True
