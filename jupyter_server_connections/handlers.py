#!/usr/bin/env python3

from jupyter_server.auth import authorized
from jupyter_server.extension.handler import ExtensionHandlerMixin
from jupyter_server.base.handlers import JupyterHandler


class DefaultHandler(ExtensionHandlerMixin, JupyterHandler):

    @authorized
    def get(self):
        pass
