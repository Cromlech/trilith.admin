# -*- coding: utf-8 -*-

from cromlech.location import get_absolute_url
from dolmen.view import View, make_layout_response as view_response
from dolmen.forms.base import form_component
from dolmen.view import view_component, context, name
from trilith.oauth2.interfaces import IClient, IClients
from trilith.oauth2.interfaces import IToken, ITokens
from trilith.oauth2.interfaces import IUser, IUsers
from . import Page, GenericIndex, tal_template
from .. import Admin


@view_component
@name('index')
@context(Admin)
class HomePage(Page):   
    template = tal_template('home.pt')


class Listing(Page):

    template = tal_template('storage.pt')
    fields = frozenset()
    link_to = link_on = 'id'
    
    def update(self):
        self.base_url = get_absolute_url(self.context, self.request)
    
    def contents(self):
        return iter(self.context)

    def describe(self, item):
        for field in self.fields:
            value = getattr(item, field.__name__, '')
            if field.__name__ == self.link_on:
                if self.link_to != self.link_on:
                    link_to = getattr(item, self.link_to)
                else:
                    link_to = value
                link = '%s/%s' % (self.base_url, link_to)
            else:
                link = None

            yield {
                'id': field.__name__,
                'link': link,
                'value': value,
            }


@form_component
@name('index')
@context(IClients)
class ClientsListing(Listing):   

    title = u"Clients"
    fields = (
        IClient['id'],
        IClient['name'],
        IClient['secret'],
    )


@view_component
@name('index')
@context(IClient)
class ClientIndex(GenericIndex):   

    @property
    def label(self):
        return u'Client: %s' % self.context.name


@view_component
@name('index')
@context(ITokens)
class TokensListing(Listing):   

    title = u"Tokens"
    fields = (
        IToken['expires'],
        IToken['client_id'],
        IToken['user_id'],
        IToken['access_token'],
        IToken['refresh_token'],
        )
    link_to = 'id'
    link_on = 'access_token'


@view_component
@name('index')
@context(IToken)
class TokenIndex(GenericIndex):   

    @property
    def label(self):
        return u'Token: %s' % self.context.access_token





@view_component
@name('index')
@context(IUsers)
class UsersListing(Listing):   

    title = u"Users"
    fields = (
            IUser['username'],
            IUser['common_name'],
            IUser['function'],
        )


