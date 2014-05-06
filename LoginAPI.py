from google.appengine.ext import ndb
import hmac

SECRET = 'fluffybunny'

class Userdb(ndb.Model):
	Username = ndb.StringProperty(indexed = True)
	Password = ndb.StringProperty()

def is_logged_in(string):
	u1 = Userdb.query(Userdb.Username == string).get()
	print u1
	if u1 == None:
		return False
	else:
		return True

def create_login_url(string):
	return '/login'

def create_logout_url(string):
	return '/logout?u=' + string

def get_current_user(string):
	u1 = Userdb.query(Userdb.Username == string).get()
	return u1.Username

def create_new_user(user,pswrd):
	usp = Userdb()
	usp.Username = user
	usp.Password = pswrd
	usp.put()
	return login(user,pswrd)

def login(user,pswrd):
	return hash_str(user)

def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()
