from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


class UserCategory(db.Model):
    username=db.StringProperty(multiline=False)
    categoryname=db.StringProperty(multiline=False)
    keywords=db.TextProperty()
    
class Article(db.Model):
    title=db.StringProperty(multiline=False)
    published_date=db.DateTimeProperty()
    link=db.StringProperty(multiline=False)
    summary=db.TextProperty()
    
class Ticker(db.Model):
    tk=db.StringProperty(multiline=False)