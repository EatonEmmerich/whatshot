from google.appengine.ext import ndb
import hmac

SECRET = 'fluffybunny'

class Userdb(ndb.Model):
	Username = ndb.StringProperty(indexed = True)
	Password = ndb.StringProperty()

def create_login_url(string):
	return '/login'

def create_logout_url(string):
	return '/logout?u=' + string

def get_current_user(string):
	u1 = Userdb.query(Userdb.Username == string).get()
	return u1.Username

def create_new_user(user,pswrd):
	usp = Userdb()
	u = hash_str(user)
	usp.Username = u
	usp.Password = hash_str(pswrd)
	usp.put()
	return login(user,pswrd)

def login(user,pswrd):
	s = hash_str(user)
	u1 = Userdb.query(Userdb.Username == s).get()
	if(is_unique_id(s) == False):
		if(u1.Password == hash_str(pswrd)):
			return s,True
		else:
			return None,False
	else:
		None,None

def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()

def is_unique_id(s):
	u1 = Userdb.query(Userdb.Username == s).get()
	if(u1 == None):
		return True
	else:
	#print 'IT\'S False!'
		return False
