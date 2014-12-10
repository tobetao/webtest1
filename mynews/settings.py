#-*-coding:utf8-*-
import jinja2
from os.path import dirname, join

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(join(dirname(__file__), 'templates')),
    extensions=['jinja2.ext.autoescape'])


WEBAPP2_CONFIG = {
    'webapp2_extras.sessions': {
        'secret_key': '\xfde\xe9\xc9\xa5z\x1e\xd8A\xf7\xc4\xc4\xc6\x8d\x89\xa0NV\xe5\xa5\n\xddOI',
    },
}


