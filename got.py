import webapp2, jinja2, os
from Crypto.Random import random
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class FirstCompare(db.Model):
    firstNum = db.FloatProperty()
    firstKey = db.IntegerProperty()
    secondKey = db.IntegerProperty()

class Result(db.Model):
    #1 - first person is greater
    #0 - equal
    #-1 - first person is less
    result = db.IntegerProperty()
    firstKey = db.IntegerProperty()
    secondKey = db.IntegerProperty()

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
        firstKey = random.getrandbits(63)
        secondKey = random.getrandbits(63)
        while FirstCompare.get_by_key_name(str(firstKey)):
            firstKey = random.getrandbits(63)
        while FirstCompare.all().filter('secondKey =', secondKey).count() > 0:
            secondKey = random.getrandbits(63)
        newFirstCompare = FirstCompare(key_name=str(firstKey),
                firstKey = firstKey,
                secondKey = secondKey,
                firstNum = number)
        newFirstCompare.put()

        #Rendering the html
        your_link = "/first?key=" + str(firstKey)
        their_link = "/second?key=" + str(secondKey)
        submitTemplate = jinja_environment.get_template('submit.html.part')
        self.response.out.write(submitTemplate.render({
            "yourlink": your_link,
            "theirlink": their_link}))

class FirstPage(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key')
        result = Result.get_by_key_name(key)
        if not result:
            self.response.out.write("Link not found. Check your link?")
        

class SecondPage(webapp2.RequestHandler):
    def get(self):
        pass
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/first', FirstPage),
                               ('/second', SecondPage)
                               ],
                               debug = True,
                               )
