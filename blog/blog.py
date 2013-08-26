import os

import webapp2
import jinja2

from google.appengine.ext import ndb

# templating engine
JINJA_ENVIRONMENT = jinja2.Environment(
loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions = ['jinja2.ext.autoescape'])


# database model
class Post(ndb.Model):
	title = ndb.StringProperty()
	text = ndb.TextProperty()
	date = ndb.DateTimeProperty(auto_now_add = True)


# handlers
class MainPage(webapp2.RequestHandler):

	def get(self):
		posts = Post.query()

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render({'posts': posts}))

class NewPostPage(webapp2.RequestHandler):

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('newpost.html')
		self.response.write(template.render())

	def post(self):
		title = self.request.get('subject')
		text = self.request.get('content')

		# input validation
		if text and title:
			post = Post()
			post.title = title
			post.text = text
			id = post.put().id()
			self.redirect('/' + str(id))
		else:
			template = JINJA_ENVIRONMENT.get_template('newpost.html')
			self.response.write(template.render({'error': "Pleaser enter text and title"}))	

class ShowPage(webapp2.RequestHandler):

	def get(self, post_id):

		post = Post.get_by_id(int(post_id))

		template = JINJA_ENVIRONMENT.get_template('show.html')
		self.response.write(template.render({'post': post}))


app = webapp2.WSGIApplication([(r'/', MainPage), (r'/newpost', NewPostPage), (r'/(\d+)', ShowPage)], debug=True)

app.run()
