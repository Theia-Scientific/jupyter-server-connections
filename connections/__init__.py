#!/usr/bin/env python3

from .app import ConnectionsExtensionApp

def _jupyter_server_extension_points():
    return [{"module": "connections.app", "app": ConnectionsExtensionApp}]
