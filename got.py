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

def greater(rh):
    rh.response.out.write('>')

def equal(rh):
    rh.response.out.write('=')

def less(rh):
    rh.response.out.write('<')

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
        newResult = Result(key_name = str(firstKey),
                           firstKey = firstKey,
                           secondKey = secondKey)
        newResult.put()

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
        if result.result == 1: #higher
            greater(self)
        elif result.result == 0:
            equal(self)
        elif result.result == -1:
            less(self)
        elif result.result == None:
            self.response.out.write("Your friend has not entered their number yet.")
        else:
            print "SOMETHING HORRIBLE WENT WRONG FIRSTPAGE"
                

class SecondPage(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key')
        try:
            key = int(key)
        except:
            self.response.out.write("Link not found. Check your link?")
            return
        result = Result.all().filter('secondKey =', key).get()
        if not result:
            self.response.out.write("Link not found. Check your link?")
            return
        secondTemplate = jinja_environment.get_template('second.html.part')
        self.response.out.write(secondTemplate.render({
            'currenturl': key}))

    def post(self):
        key = self.request.get('key')
        try:
            key = int(key)
        except:
            self.response.out.write("Link not found. Check your link?")
            return
        result = Result.all().filter('secondKey =', key).get()
        comp = FirstCompare.all().filter('secondKey =', key).get()
        if not result:
            self.response.out.write("Link not found. Check your link?")
            return
        number = self.request.get('number')
        try:
            number = float(number)
        except:
            self.response.out.write("You didn't give a number.")
            return
        if comp.firstNum > number:
            result.result = 1
        elif comp.firstNum < number:
            result.result = -1
        elif comp.firstNum == number:
            result.result = 0
        result.put()
        comp.delete()
        self.redirect('/third?key=' + str(key))
    

class ThirdPage(webapp2.RequestHandler):
    def get(self):
        key = self.request.get('key')
        try:
            key = int(key)
        except:
            self.response.out.write("Link not found.")
            return
        result = Result.all().filter('secondKey =', key).get()
        if not result:
            self.response.out.write("Link not found.")
            return
        if result.result == -1:
            greater(self)
        elif result.result == 0:
            equal(self)
        elif result.result == 1:
            less(self)
        
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/first', FirstPage),
                               ('/second', SecondPage),
                               ('/third', ThirdPage)
                               ],
                               debug = True,
                               )
