# -*- coding: utf-8 -*-

from os import path
from dolmen.template import TALTemplate
from dolmen.message.interfaces import BASE_MESSAGE_TYPE
from dolmen.view import View, make_layout_response as view_response
from cromlech.webob import Response


ERROR_MESSAGE_TYPE = u'error'


TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')


def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))


class Page(View):   
    responseFactory = Response
    make_response = view_response
