import os
import cgi
from itertools import chain
import json
import urllib
import logging
import pprint
from models import *

from google.appengine.api import users
import webapp2
from webapp2_extras import auth, sessions

from .base import BaseHandler, LoginRequiredHandler
from AccessDB import getMyNews, getCategories, updateCategories
from helpers import get_template
from settings import WEBAPP2_CONFIG


class MyNewsView(LoginRequiredHandler):

    def get(self):
        user_id = self.context.get('user_id')
        categories = getCategories(user_id)
        self.context.update({
            'categories': categories,
        })
        template = get_template('mynews.html')
        self.response.write(template.render(self.context))


class GetNewsView(LoginRequiredHandler):

    def get(self):
        user_id = self.context.get('user_id')
        news = getMyNews(user_id)
        self.context.update({
            'category_news_left': news['CATEGORY'][len(news['CATEGORY'])/2:],
            'category_news_right': news['CATEGORY'][:len(news['CATEGORY'])/2],
            'realtime_news_list': news['REAL TIME'],
        })
        template = get_template('news.html')
        self.response.write(template.render(self.context))


class CategoryView(LoginRequiredHandler):

    def get(self):
        user_id = self.context.get('user_id')
        categories = getCategories(user_id)
        self.context.update({
            'categories': categories,
        })
        template = get_template('category.html')
        self.response.write(template.render(self.context))

    def post(self):
        categories = {}
        for k in self.request.arguments():
            v = self.request.get(k, '').strip().split(' ')
            if k and v:
                categories[k] = v

        mycats=db.GqlQuery("select * from UserCategory where username='%s'" % self.context.get('user_id'))
        for mycat in mycats:    mycat.delete()
        for key, value in categories.iteritems():
            #print self.context.get('user_id'), key, ' '.join(map(str, value))
            mycategory=UserCategory(username=self.context.get('user_id'), categoryname=key, keywords=' '.join(map(unicode, value)))
            mycategory.put()
        user_id = self.context.get('user_id')
        updateCategories(user_id, categories)
        self.response.write('OK')


app = webapp2.WSGIApplication([
    ('/', MyNewsView),
    ('/getnews/', GetNewsView),
    ('/category/', CategoryView),
],
config=WEBAPP2_CONFIG,
debug=True)

