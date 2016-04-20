# -*- coding: utf-8 -*-

from os import path
from dolmen.forms.base import Form, DISPLAY
from dolmen.template import TALTemplate
from dolmen.message.interfaces import BASE_MESSAGE_TYPE
from dolmen.view import View, make_layout_response as view_response
from dolmen.forms.base.components import make_layout_response as form_response
from cromlech.webob import Response
from dolmen.forms.base import Fields


ERROR_MESSAGE_TYPE = u'error'


TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')


def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))


class Page(View):   
    responseFactory = Response
    make_response = view_response


class GenericIndex(Form):

    mode = DISPLAY
    ignoreRequest = True
    ignoreContent = False

    responseFactory = Response
    make_response = form_response
    action_url = "."
    
    @property
    def fields(self):
        return Fields(*self.context.__schema__)
