# -*- coding: utf-8 -*-

from cromlech.location import get_absolute_url
from dolmen.view import View, make_layout_response as view_response
from dolmen.forms.base import form_component
from dolmen.view import view_component, context, name
from trilith.oauth2.interfaces import IClient, IClients
from trilith.oauth2.interfaces import IToken, ITokens
from trilith.oauth2.interfaces import IUser, IUsers
from trilith.oauth2.interfaces import IGrant, IGrants
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
    links = {}
    
    def contents(self):
        return iter(self.context)

    def describe(self, item):
        for field in self.fields:
            name = field.__name__
            value = getattr(item, name, '')
            if field.__name__ in self.links:
                link = self.links[name].format(self.request.script_name, item)
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
    links = {
        'name': '{0}/clients/{1.id}',
        }
    

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
    links = {
        'access_token': '{0}/tokens/{1.id}',
        'client_id': '{0}/clients/{1.client_id}',
        }


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
    links = {
        'username': '{0}/users/{1.username}',
        }


@view_component
@name('index')
@context(IUser)
class UserIndex(GenericIndex):   

    @property
    def label(self):
        return u'User: %s' % self.context.username


@view_component
@name('index')
@context(IGrants)
class GrantsListing(Listing):   

    title = u"Grants"
    fields = (
            IGrant['client_id'],
            IGrant['user_id'],
            IGrant['code'],
            IGrant['scopes'],
        )
    links = {
        'code': '{0}/grants/{1.id}',
        'user_id': '{0}/users/{1.user_id}',
        'client_id': '{0}/clients/{1.client_id}',
        }


@view_component
@name('index')
@context(IGrant)
class GrantIndex(GenericIndex):   

    @property
    def label(self):
        return u'Grant: %s' % self.context.code
