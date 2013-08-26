import webapp2
import re
import os
import jinja2
import hashlib

from google.appengine.ext import ndb

# templating engine
JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'])

class User(ndb.Model):
	name = ndb.StringProperty(required = True)
	password = ndb.StringProperty(required = True)
	email = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(pw):
	return PW_RE.match(pw)

MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return MAIL_RE.match(email)

def build_cookie_val(id):
	hash = hashlib.sha256(str(id) + "cool").hexdigest()
	return '%s|%s' % (id, hash)

def valid_cookie(hash):
	li = hash.split('|')
	if build_cookie_val(li[0]) == hash:
		return li[0]
	

class MainPage(webapp2.RequestHandler):

	def write_form(self, e1, e2, e3, e4, user, email):
		x = {
			'err_user': e1,
			'err_pw': e2,
			'err_verify': e3,
			'err_email': e4, 
			'user': user,
			'email': email
		}

		template = JINJA_ENVIRONMENT.get_template('registration.html')
		self.response.write(template.render(x))

	def get(self):
		self.write_form("","","","","","")

	def post(self):
		e1 = ""
		e2 = ""
		e3 = ""
		e4 = ""
		flag = 0

		user = self.request.get("username")
		email = self.request.get("email")
		pw = self.request.get("password")
		verify = self.request.get("verify")

		if not valid_username(user):
			e1 = "invalid username"
			flag = 1

		if not valid_password(pw):
			e2 = "invalid password"
			flag = 1

		if not pw == verify:
			e3 = "pw doens't match"
			flag = 1

		if not valid_email(email) and not email == "":
			e4 = "invalid email"
			flag = 1

		if flag == 1:
			self.write_form(e1, e2, e3, e4, user, email)
		else:
			u = User()
			u.name = user
			u.password = hashlib.sha256(pw).hexdigest()
			if email:
				u.email = email
			key = u.put()

			id = str(key.id())		
			self.response.set_cookie('user_id', build_cookie_val(id))
			self.redirect("/welcome")

class WelcomePage(webapp2.RequestHandler):

	def get(self):
		hashed_val = self.request.cookies.get('user_id','-1')

		if hashed_val == '-1':
			self.redirect('/signup')
		else:
			id = valid_cookie(hashed_val)
			if id != None:
				u = User.get_by_id(int(id))
				template = JINJA_ENVIRONMENT.get_template('welcome.html')
				self.response.write(template.render({'name': u.name}))
			else:
				self.redirect('/signup')

class LoginPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('login.html')
		self.response.write(template.render())

	def post(self):
		name = self.request.get('username')
		password = self.request.get('password')

		if name and password:
			query = User.query(User.name == name)
			for u in query:
				if u.password == hashlib.sha256(password).hexdigest():
					self.response.set_cookie('user_id', build_cookie_val(u.key.id()))
					self.redirect('/welcome')
				else:
					template = JINJA_ENVIRONMENT.get_template('login.html')
					self.response.write(template.render())				

		else:
			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render())

class LogoutPage(webapp2.RequestHandler):
	def get(self):
		self.response.delete_cookie('user_id')
		self.redirect('/signup')

app = webapp2.WSGIApplication([('/signup', MainPage), ('/welcome', WelcomePage), ('/login', LoginPage), ('/logout', LogoutPage)], debug=True)

app.run()
