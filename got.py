import webapp2, jinja2, os
from Crypto.Random import random

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        indexTemplate = jinja_environment.get_template('index.html.part')
        self.response.out.write(indexTemplate.render())

    def post(self):
        number = self.request.get('number')
        try:
            number = float(number)
        except:
            self.response.out.write("You should enter an actual number.\n"
                                    "Any decimal number is acceptable.\n"
                                    '<a href="/">Return.</a>')
            return
        #Generate two random numbers, check if they're already there,
        #commit it into the datastore and give the guy links
app = webapp2.WSGIApplication([('/', MainPage),
                               ],
                               debug = True,
                               )
