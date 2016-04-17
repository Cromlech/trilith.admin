# -*- coding: utf-8 -*-

from cromlech.location import get_absolute_url
from dolmen.view import View, make_layout_response as view_response
from dolmen.view import view_component, context, name
from trilith.oauth2.interfaces import IClient, IClients
from . import Page, tal_template
from .. import Admin


@view_component
@name('index')
@context(Admin)
class HomePage(Page):   
    template = tal_template('home.pt')


class Listing(Page):

    template = tal_template('storage.pt')
    fields = frozenset()

    def update(self):
        self.base_url = get_absolute_url(self.context, self.request)
    
    def contents(self):
        return iter(self.context)

    
@view_component
@name('index')
@context(IClients)
class ClientsListing(Listing):   

    title = u"Clients"
    fields = frozenset(
        (IClient['id'],
         IClient['name'],
         IClient['secret']))

    def describe(self, item):
        for field in self.fields:
            if field.__name__ == 'id':
                link = '%s/%s' % (self.base_url, item.id)
            else:
                link = None
            value = getattr(item, field.__name__, '')
            yield {
                'id': field.__name__,
                'link': link,
                'value': value,
            }


@view_component
@name('index')
@context(IClient)
class ClientIndex(Page):   
    
    def render(self):
        return u'bloup'
