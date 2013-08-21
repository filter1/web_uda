import webapp2, re

form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%s">
          </td>
          <td class="error">
            %s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%s">
          </td>
          <td class="error">
            %s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

welcome = """
<h1>Welcome %s </h1>
"""


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
  return USER_RE.match(username)

PW_RE = re.compile(r"^.{3,20}$")
def valid_password(pw):
  return PW_RE.match(pw)

MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return MAIL_RE.match(email)



class MainPage(webapp2.RequestHandler):

	def write_form(self, e1, e2, e3, e4, user, email):
		self.response.write(form % (user, e1, e2, e3, email, e4))

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
			self.redirect("/welcome?username=" + user)

class WelcomePage(webapp2.RequestHandler):

	def get(self):
		user = self.request.get("username")
		self.response.write(welcome % user)


app = webapp2.WSGIApplication([('/', MainPage),('/welcome', WelcomePage)], debug=True)

app.run()
