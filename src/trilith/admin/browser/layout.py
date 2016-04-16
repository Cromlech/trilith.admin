# -*- coding: utf-8 -*-

import crom

from cromlech.browser import IRequest, ILayout
from cromlech.i18n import getLocalizer
from cromlech.webob import Response
from dolmen.message.utils import receive as receive_messages
from dolmen.viewlet import ViewletManager, viewlet_manager
from zope.interface import Interface
from . import BASE_MESSAGE_TYPE, ERROR_MESSAGE_TYPE, tal_template


@viewlet_manager
class AboveBody(ViewletManager):
    pass


@crom.component
@crom.sources(IRequest, Interface)
@crom.target(ILayout)
class BaseLayout(object):
    responseFactory = Response
    template = tal_template('layout.pt')

    title = u"Trilith: Administration"

    def __init__(self, request, context):
        self.context = context
        self.request = request

    @property
    def translate(self):
        """Returns the current localizer using the thread cache.
        Please note that the cache might be 'None' if nothing was set up.
        None will, most of the time, mean 'no translation'.
        """
        localizer = getLocalizer()
        if localizer is not None:
            localizer.translate
        return None
        
    def namespace(self, **extra):
        namespace = {
            'context': self.context,
            'request': self.request,
            'layout': self,
            'user': self.request.environment.get('REMOTE_USER'),
            'messages': list(receive_messages(type=BASE_MESSAGE_TYPE) or []),
            'errors': list(receive_messages(type=ERROR_MESSAGE_TYPE) or []),
            }
        namespace.update(extra)
        return namespace

    def __call__(self, content, **namespace):
        environ = self.namespace(content=content, **namespace)
        return self.template.render(self, translate=self.translate, **environ)
