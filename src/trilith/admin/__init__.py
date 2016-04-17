# -*- coding: utf-8 -*-

import ConfigParser
import logging

from crom import monkey, implicit
from cromlech.configuration.utils import load_zcml
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from cromlech.i18n import Locale, load_translations_directories
from cromlech.i18n import get_localizer, get_environ_language
from cromlech.browser.interfaces import IPublicationRoot
from cromlech.webob import Request
from cromlech.dawnlight import traversable
from zope.interface import implementer, directlyProvides
from zope.location import Location, ILocation, LocationProxy
from barrel import cooper


PUBLISHER = DawnlightPublisher(
    view_lookup=ViewLookup(view_locator(query_view)),
    )


@traversable('users', 'clients', 'grants', 'tokens')
@implementer(IPublicationRoot)
class Admin(Location):

    def __init__(self, users, clients, grants, tokens):
        self.users = LocationProxy(users, self, 'users')
        self.clients = LocationProxy(clients, self, 'clients')
        self.grants = LocationProxy(grants, self, 'grants')
        self.tokens = LocationProxy(tokens, self, 'tokens')


def manager(accesses, zcml_file, users, clients, grants, tokens):

    # Read users
    config = ConfigParser.ConfigParser()
    config.read(accesses)
    admin_accesses = config.items('admin')

    # load crom
    monkey.incompat()
    implicit.initialize()

    # Grokking trigger
    load_zcml(zcml_file)
    
    @cooper.basicauth(users=admin_accesses, realm='TrilithAdmin')
    def admin_ui(environ, start_response):
        locale = get_environ_language(environ) or 'fr_FR'
        localizer = get_localizer(locale)

        with Locale(locale, localizer):
            request = Request(environ)
            root = Admin(users, clients, grants, tokens)
            response = PUBLISHER.publish(request, root, handle_errors=False)
            return response(environ, start_response)

    return admin_ui
