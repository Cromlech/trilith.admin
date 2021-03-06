# -*- coding: utf-8 -*-

from crom import order
from cromlech.location import get_absolute_url
from cromlech.browser.directives import title
from cromlech.browser import name, exceptions, request, IResponse
from cromlech.browser.exceptions import HTTPRedirect
from cromlech.browser.utils import redirect_exception_response
from cromlech.webob import Response

from dolmen.forms.base import set_fields_data
from dolmen.forms.base import FAILURE, action, Form, Fields, SuccessMarker
from dolmen.forms.base import form_component, name, action, utils
from dolmen.forms.base.components import make_layout_response as form_response
from dolmen.forms.base.errors import Errors, Error
from dolmen.forms.ztk.validation import InvariantsValidation
from dolmen.message import send as website_message
from dolmen.view import view_component, context

from webob.exc import HTTPFound
from zope.interface import Interface

from trilith.oauth2.interfaces import IStorage, IClient, IUser
from . import tal_template


@view_component
@name('add')
@order(2)
@context(IStorage)
class Add(Form):

    ignoreContent = True
    ignoreRequest = False

    responseFactory = Response
    make_response = form_response
    label = u"Add"
    dataValidators = [InvariantsValidation]

    template = tal_template('form.pt')
    
    @property
    def fields(self):
        return Fields(*self.context.__factory__.__schema__)

    @property
    def action_url(self):
        return self.request.url

    @action(u"Create")
    def create(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE
        item = self.context.add(**data)
        action_url = str(get_absolute_url(self.context, self.request))
        raise exceptions.HTTPFound(location=action_url)

    @action(u"Cancel")
    def cancel(self):
        action_url = str(self.request.script_name)
        raise exceptions.HTTPFound(location=action_url)


class Edit(Form):

    ignoreContent = False
    ignoreRequest = False

    responseFactory = Response
    make_response = form_response
    label = u"Edit"
    dataValidators = [InvariantsValidation]

    template = tal_template('form.pt')
    
    @property
    def fields(self):
        return Fields(*self.context.__schema__)

    @property
    def action_url(self):
        return self.request.url

    @action(u"Update")
    def save_changes(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE
        self.context.__parent__.update(self.context, **data)
        action_url = str(get_absolute_url(self.context, self.request))
        raise exceptions.HTTPFound(location=action_url)

    @action(u"Cancel")
    def cancel(self):
        action_url = str(self.request.script_name)
        raise exceptions.HTTPFound(location=action_url)


@view_component
@order(2)
@name('edit')
@title('Edit')
@context(IClient)
class ClientEdit(Edit):
    
    @property
    def fields(self):
        fields = Fields(*self.context.__schema__)
        fields['id'].readonly = True 
        fields['name'].readonly = True 
        return fields


@view_component
@order(2)
@name('edit')
@title('Edit')
@context(IUser)
class UserEdit(Edit):
    
    @property
    def fields(self):
        fields = Fields(*self.context.__schema__)
        fields['username'].readonly = True
        return fields
