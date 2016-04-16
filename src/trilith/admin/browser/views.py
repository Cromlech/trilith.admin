# -*- coding: utf-8 -*-

from dolmen.view import View, make_layout_response as view_response
from dolmen.view import view_component, context, name
from trilith.oauth2.interfaces import IStorage
from . import Page, tal_template
from .. import Admin


@view_component
@name('index')
@context(Admin)
class HomePage(Page):   
    template = tal_template('home.pt')


@view_component
@name('index')
@context(IStorage)
class HomePage(Page):   
    template = tal_template('storage.pt')

    def update(self):
        self.content = iter(self.context)
