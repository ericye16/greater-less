import webapp2, jinja2, os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
    def get(self):
        indexTemplate = jinja_environment.get_template('index.html')
        self.response.out.write(indexTemplate.render())

    def post(self):
        number = self.request.get('number')
        

app = webapp2.WSGIApplication([('/', MainPage),
                               ],
                               debug = True,
                               )
