import urllib, pprint
from bs4 import BeautifulSoup
from dateutil import parser
from datetime import date, datetime, timedelta

import urllib2, sys
import cookielib
import feedparser  
import codecs
import time, os, os.path
import random

from sp500 import sp500
from sse import sse
from alltks import alltks

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from models import *

class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        feed="https://www.google.com/finance/company_news?q=NASDAQ:CLDX&ei=XSlwU7CfGqHm6AH5xoCAAw&output=rss"
        sp500feed="https://www.google.com/finance/company_news?q=%s&output=rss&random=%s"
        ssefeed="https://www.google.com/finance/company_news?q=%s&gl=cn&output=rss&random=%s"
        #alltks=sp500+sse
        global alltks
        if 'mynewscn' in os.path.dirname(os.path.abspath(__file__)):
            alltks=sse
        
        tks_per_sessin=5
        
        processedTks=db.GqlQuery("select * from Ticker")
        oldTks=set([tk.tk for tk in processedTks])
        todoTks=[i for i in alltks if i not in oldTks]
        if len(todoTks)==0:
            for t in Ticker.all():  t.delete()
            todoTks=alltks[:]
            
        try:
            tkssession=random.sample(todoTks, tks_per_sessin)
        except:
            tkssession=todoTks[:]
        for t in tkssession:
            processedTk=Ticker(tk=t)
            processedTk.put()
            
        #delete old articles
        year=(datetime.today()-timedelta(7)).year
        month=(datetime.today()-timedelta(7)).month
        day=(datetime.today()-timedelta(7)).day
        expirearticles=db.GqlQuery("select * from Article where published_date < DATETIME(%s, %s, %s, 0, 0, 0) " % (year, month, day))
        for i in expirearticles:
            i.delete()
        
        for i, tk in enumerate(tkssession):
            if len(tk)==6:
                feed=ssefeed % (tk, str(time.time()))
            else:
                feed=sp500feed % (tk, str(time.time()))
            try:
                d = feedparser.parse(feed) 
                for e in d.entries:
                    self.response.out.write("%s, %s\n" % (tk, str(i)))
                    title=e.title
                    published_date=parser.parse(e['published'])
                    self.response.out.write(published_date)
                    self.response.out.write(date.today())
                    self.response.out.write("\n")
#                     self.response.out.write(published_date<date.today())
                    self.response.out.write("\n")
                    if published_date.date()< date.fromordinal(date.today().toordinal()-1):
                        continue
                    link=e['link']
                    summary=BeautifulSoup(e['summary_detail']['value']).get_text().replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n').replace('\n\n', '\n')
                    oldarticles=db.GqlQuery("select * from Article where link='%s' " % link)
                    oldarticles2=db.GqlQuery("select * from Article where title='%s' " % title)
                    if len(list(oldarticles))==0 and len(list(oldarticles2))==0:
                        article=Article(title=title, published_date=published_date, link=link, summary=summary)
                        article.put()
            except:     pass
        
#         usercategory=UserCategory(username='damingli', categoryname='computer', keywords=unicode('f'))
#         usercategory.put()
#         usercategories=db.GqlQuery("select * from UserCategory where username='damingli' ")
#         for usercategory in usercategories:
#             usercategory.delete()

# 
#         articles=db.GqlQuery("select * from Article")
#         for article in articles:
#             article.delete()
        

        
#         self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
        
class DeletePage(webapp.RequestHandler):
    
    
    def get(self):        
        for article in Article.all():
            article.delete()        
        for tk in Ticker.all():
            tk.delete()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
        
class DeleteAllPage(webapp.RequestHandler):
    
    
    def get(self):        
        for article in Article.all():
            article.delete()        
        for tk in Ticker.all():
            tk.delete()
        for c in UserCategory.all():
            c.delete()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')


application = webapp.WSGIApplication([('/refresh', MainPage), ('/delete', DeletePage), ('/deleteall', DeleteAllPage)], debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
