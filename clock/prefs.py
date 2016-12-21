import webapp2
import models

class PrefsPage(webapp2.RequestHandler):
	def post(self):
		userprefs = models.get_userprefs()
		try:
			tz_offset = int(self.request.get('tz_offset'))
			userprefs.tz_offset = tz_offset
			userprefs.put()
		except ValueError:
			# User entered a value that wasnt an integer. Ignore for now.
			pass

		self.redirect('/')

application = webapp2.WSGIApplication([('/prefs', PrefsPage)], debug=True)
