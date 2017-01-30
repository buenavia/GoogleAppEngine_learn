import webapp2
import models

class PrefsPage(webapp2.RequestHandler):
	def get(self):
		self.redirect('/')

application = webapp2.WSGIApplication([('/test', PrefsPage)], debug=True)
