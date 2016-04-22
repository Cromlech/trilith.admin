# -*- coding: utf-8 -*-

import crom
from crom.utils import sort_components
from cromlech.location import get_absolute_url
from cromlech.browser import IRequest, ILayout, IView
from cromlech.browser.directives import title
from cromlech.i18n import getLocalizer
from cromlech.webob import Response
from dolmen.message.utils import receive as receive_messages
from dolmen.viewlet import ViewletManager, viewlet_manager
from zope.interface import Interface
from . import BASE_MESSAGE_TYPE, ERROR_MESSAGE_TYPE, tal_template


def sorter(component):
    explicit = crom.order.get_policy(component[1], crom.order.dotted_name, 0)
    return (explicit, component[1].__module__, component[0])


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

    def get_tabs(self, view=None):
        tabs = []
        base_url = get_absolute_url(self.context, self.request)
        if view is not None:
            current = (crom.name.get(view), view.__class__)
        for name, klass in sort_components(
                IView.all_components(self.context, self.request), key=sorter):
            tabs.append({
                'id': name,
                'title': title.get(klass) or name,
                'selected': current == (name, klass),
                'url': '%s/%s' % (base_url, name),
                })
        if len(tabs) == 1 and tabs[0]['selected']:
            return []
        return tabs

    def namespace(self, **extra):
        extra['tabs'] = self.get_tabs(extra.get('view'))
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
