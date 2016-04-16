# -*- coding: utf-8 -*-

from cromlech.browser import name, exceptions, request, IResponse
from cromlech.browser.exceptions import HTTPRedirect
from cromlech.browser.utils import redirect_exception_response
from cromlech.webob import Response

from dolmen.forms.base import FAILURE, action, Form, Fields, SuccessMarker
from dolmen.forms.base import form_component, name, action, utils
from dolmen.forms.base.components import make_layout_response as form_response
from dolmen.forms.base.errors import Errors, Error
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.message import send as website_message
from dolmen.view import View, make_layout_response as view_response
from dolmen.view import view_component, context

from webob.exc import HTTPFound
from zope.interface import Interface

from . import tal_template


@view_component
@name('add')
@context(Interface)
class Add(Form):

    ignoreContent = True
    ignoreRequest = False

    responseFactory = Response
    make_response = form_response
    label = u"Ajout"
    dataValidators = [InvariantsValidation]

    template = tal_template('form.pt')
    
    @property
    def fields(self):
        return Fields()

    @property
    def action_url(self):
        return self.request.url

    @action(u"Créer")
    def create(self):
        pass
        
    @action(u"Annuler")
    def cancel(self):
        action_url = str(self.request.script_name)
        raise exceptions.HTTPFound(location=action_url)
