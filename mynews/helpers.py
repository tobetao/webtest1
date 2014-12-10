#-*-coding:utf8-*-

from settings import JINJA_ENVIRONMENT


def get_template(template_name):
    return JINJA_ENVIRONMENT.get_template(template_name)

