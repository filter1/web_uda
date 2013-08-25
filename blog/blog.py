import os

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Evironment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions = ['jinja2.ext.autoescape'])


class MainPage(webapp2.RequestHandler):

class NewPostPage(webapp2.RequestHandler):

class ShowPage(webapp2.RequestHandler):



app = webapp2.WSGIApplication([(r'/', MainPage), (r'/newpost', NewPostPage), (r'/(\d+)', ShowPage)], debug=True)

app.run()
