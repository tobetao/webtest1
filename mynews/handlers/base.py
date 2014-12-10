import os
import cgi
import json
import urllib
import logging

from google.appengine.api import users
import webapp2
from webapp2_extras import auth, sessions

from settings import JINJA_ENVIRONMENT, WEBAPP2_CONFIG
from .mixins import LoginRequiredMixin, AdminRequiredMixin


class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            logging.debug('==== save session ====')
            self.session_store.save_sessions(self.response)


class LoginRequiredHandler(LoginRequiredMixin, BaseHandler):
    pass

class AdminRequiredHandler(LoginRequiredMixin, AdminRequiredMixin, BaseHandler):
    pass
