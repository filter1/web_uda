import webapp2, cgi

form = """
<h2>Enter some text to ROT13:</h2>
<form method="post">
	<textarea name="text"
						style="height: 100px; width: 400px;">
	%(text)s
	</textarea>
	<br>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form(self, text = ""):
		self.response.out.write(form % {"text": text})

	def encode(self, text):
		res = ''

		for c in text:
			a = ord(c) # ascii

			if a in range(65, 91):
				a += 13
				if a > 90: # overflow
					a = 65 + a - 91

			if a in range(97, 123):
				a += 13
				if a > 122:
					a = 97 + a - 123

			res += chr(a)
		return res

	def get(self):
		self.write_form()


	def post(self):
		encoded_text = self.encode(self.request.get('text'))
		escaped_text = cgi.escape(encoded_text)
		self.write_form(escaped_text)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

app.run()
