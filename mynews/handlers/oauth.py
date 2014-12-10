#-*-coding:utf8-*-
import cgi
import json
import urllib
import logging
import socket, os, os.path

import webapp2
from webapp2_extras import auth, sessions
from google.appengine.api import urlfetch

from .base import BaseHandler
from settings import JINJA_ENVIRONMENT, WEBAPP2_CONFIG

OAUTH_CLIENT_ID = '574019-q83p6k2r4gdgfmesotm5l8oj29uvhkqh.apps.googleusercontent.com'
OAUTH_CLIENT_SECRET = '4rlcA7drmd2jF3n8N3-'
OAUTH_REDIRECT_URI = 'http://localhost:8080/code'

# toptodayus appspot
# OAUTH_CLIENT_ID = '574018215629-8o1ftevu42085jrrgn8e42c62b8p4s6m.apps.googleusercontent.com'
# OAUTH_CLIENT_SECRET = 'Gfd2x25HXgU5ij05O65mCh0S'
# OAUTH_REDIRECT_URI = 'http://toptodayus.appspot.com/code'

# d11-01
if 'D11-01' in socket.gethostname():
    OAUTH_CLIENT_ID = '574018215629-e7cdf9lmkttj486m0d8m7pr6uipns.apps.googleusercontent.com'
    OAUTH_CLIENT_SECRET = 'NT352DzEI-bdmTYA5ZCbGN'
    OAUTH_REDIRECT_URI = 'http://d11-01.fxdd.com:8080/code'
    if 'mynewscn' in os.path.dirname(os.path.abspath(__file__)):
        OAUTH_CLIENT_ID = '574018215629-cil2lc0k4pjhocb592ajk29crtmt8.apps.googleusercontent.com'
        OAUTH_CLIENT_SECRET = '_nXNWsd4bIbqBMMMIb08E'
        OAUTH_REDIRECT_URI = 'http://d11-01.fxdd.com:8081/code'

OAUTH_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
]
OAUTH_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
OAUTH_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
OAUTH_USERINFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'


class OAuthLogin(BaseHandler):

    def get(self):
        context = {
            'auth_url': OAUTH_AUTH_URL,
            'client_id': OAUTH_CLIENT_ID,
            'scope': ' '.join(OAUTH_SCOPE),
            'redirect_uri': OAUTH_REDIRECT_URI,
            'continue': self.request.get('continue', '/')
        }
        template = JINJA_ENVIRONMENT.get_template('oauth_login.html')
        self.response.write(template.render(context))


class OAuthLogout(BaseHandler):
    def get(self):
        a = auth.get_auth()
        a.unset_session()
        self.redirect('/')


class OAuthCallback(BaseHandler):

    def get(self):
        if 'error' in self.request.GET:
            self.response.write('Failed to authenticate.')
            return
        code = cgi.escape(self.request.get('code'))
        form_fields = {
                'code': code,
                'client_id': OAUTH_CLIENT_ID,
                'client_secret': OAUTH_CLIENT_SECRET,
                'redirect_uri': OAUTH_REDIRECT_URI,
                'grant_type': 'authorization_code',
            }
        form_data = urllib.urlencode(form_fields)
        result = urlfetch.fetch(
                        OAUTH_TOKEN_URL,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'}
                    )
        result = result.content
        logging.info('===== result ====%s' % result)
        result = json.loads(result)
        access_token = result['access_token']
        userinfo_url = OAUTH_USERINFO_URL + '?access_token=%s' % access_token
        info = urlfetch.fetch(
                        userinfo_url,
                        method=urlfetch.GET,
                    )
        info = info.content
        logging.info('get user info ...%s' % info)
        info = json.loads(info)
        if not info['email'].endswith('gmail.com'):
            self.error(403)
            self.write('You don\'t have access.')
            return
        self.set_logged_in(info)
        state = cgi.escape(self.request.get('state'))
        self.redirect('/')

    def set_logged_in(self, info):
        auth_id = '%s:%s' % ('google', info['id'])
        a = auth.get_auth()
        user = a.store.user_model.get_by_auth_id(auth_id)
        if user:
            user.put()
            logging.debug('...... user exists .... set_session')
            a.set_session(a.store.user_to_dict(user))
        else:
            logging.debug('...... user dost not exist ....')
            if a.get_user_by_session():
                logging.info('User is already logged in.')
            else:
                logging.info('Create new user.')
                attrs = {
                    'name': info['name'],
                    'email': info['email'],
                }
                ok, user = a.store.user_model.create_user(auth_id, **attrs)
                logging.debug('...... user create ....%s' % str(ok))
                if ok:
                    logging.debug('...... user create OK ... set_session....%s')
                    a.set_session(a.store.user_to_dict(user))



app = webapp2.WSGIApplication([
    ('/_ah/login_required', OAuthLogin),
    ('/logout', OAuthLogout),
    ('/code', OAuthCallback),
],
config=WEBAPP2_CONFIG,
debug=True)
