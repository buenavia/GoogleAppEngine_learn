import jinja2
import os
import webapp2
import json

from google.appengine.api import users
from google.appengine.ext import ndb

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

class Book(ndb.Model):
	id = ndb.IntegerProperty()
	title = ndb.StringProperty()
	isbn = ndb.StringProperty()
	genre = ndb.StringProperty(repeated = True)
	author = ndb.StringProperty()
	checkedIn = ndb.BooleanProperty()		

class Customer(ndb.Model):
	id = ndb.IntegerProperty()
	name = ndb.StringProperty()
	balance = ndb.FloatProperty()
	checked_out = ndb.StringProperty(repeated=True)

class BookHandler(webapp2.RequestHandler):
	def post(self):
		book_data = json.loads(self.request.body)
		new_book = Book(
			id = book_data['id'],
			title=book_data['title'],
			isbn=book_data['isbn'],
			genre=book_data['genre'],
			author=book_data['author'], 
			checkedIn=book_data['checkedIn'])	#when testing, needs to be lower case e.g. true
			
		new_book.put() 									#Model section of NDB docs

		#self-links
		#Keys
		book_dict = new_book.to_dict()
		book_dict['self'] = '/book/' + new_book.key.urlsafe()

		self.response.write(json.dumps(book_dict))

	def get(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			b_dict = b.to_dict()
			b_dict['self'] = "/book/" + id
			self.response.write(json.dumps(b_dict))

	def put(self, id=None):
		if id:

			book_data = json.loads(self.request.body)

			b = ndb.Key(urlsafe=id).get()

			b.id = book_data['id']
			b.title=book_data['title']			
			b.isbn=book_data['isbn']
			b.genre=book_data['genre']
			b.author=book_data['author']
			b.checkedIn=book_data['checkedIn']

			b_dict = b.to_dict()
			b_dict['self'] = "/book/" + id
			self.response.write(json.dumps(b_dict))

	def delete(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			b.key.delete()

	def patch(self, id=None):
		if id:
			book_data = json.loads(self.request.body)

			b = ndb.Key(urlsafe=id).get()

			b.id = book_data['id']
			b.title=book_data['title']			
			b.isbn=book_data['isbn']
			b.genre=book_data['genre']
			b.author=book_data['author']
			b.checkedIn=book_data['checkedIn']

			b_dict = b.to_dict()
			b_dict['self'] = "/book/" + id
			self.response.write(json.dumps(b_dict))

class CustomerHandler(webapp2.RequestHandler):
	def post(self):
		cust_data = json.loads(self.request.body)
		new_cust = Customer(
			id = cust_data['id'],
			name=cust_data['name'],
			balance=cust_data['balance'],
			checked_out=cust_data['checked_out'])	#when testing, needs to be lower case e.g. true
			
		new_cust.put() 									#Model section of NDB docs			

		cust_dict = new_cust.to_dict()
		cust_dict['self'] = '/customer/' + new_cust.key.urlsafe()

		self.response.write(json.dumps(cust_dict))

	def get(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			b_dict = b.to_dict()
			b_dict['self'] = "/book/" + id
			self.response.write(json.dumps(b_dict))

	def put(self, id=None):
		if id:

			book_data = json.loads(self.request.body)

			b = ndb.Key(urlsafe=id).get()

			b.id = cust_data['id']
			b.title=book_data['title']			
			b.isbn=book_data['isbn']
			b.genre=book_data['genre']
			b.author=book_data['author']
			b.checkedIn=book_data['checkedIn']

			b_dict = b.to_dict()
			b_dict['self'] = "/book/" + id
			self.response.write(json.dumps(b_dict))

	def delete(self, id=None):
		if id:
			b = ndb.Key(urlsafe=id).get()
			b.key.delete()

	def patch(self, id=None):
		if id:
			book_data = json.loads(self.request.body)

			b = ndb.Key(urlsafe=id).get()

			b.id = cust_data['id']
			b.title=book_data['title']			
			b.isbn=book_data['isbn']
			b.genre=book_data['genre']
			b.author=book_data['author']
			b.checkedIn=book_data['checkedIn']

			b_dict = b.to_dict()
			b_dict['self'] = "/custmer/" + id
			self.response.write(json.dumps(b_dict))

class CustomerBooksHandler(webapp2.RequestHandler):
	def get(self, id=None):
		if id:
			q = Customer.query().filter(Customer.id == int(id))
			results = q.fetch()

			self.response.write(results)

# [START main_page]
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("hello")
# [END main_page]

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
application = webapp2.WSGIApplication([
    ('/', MainPage),
	('/book', BookHandler),
	('/book/(.*)', BookHandler),
	('/customer', CustomerHandler),
	('/customer/(.*?)/books', CustomerBooksHandler),
	('/customer/(.*)', CustomerHandler)
], debug=True)
# [END app]
