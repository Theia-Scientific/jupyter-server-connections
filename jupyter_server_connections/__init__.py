#!/usr/bin/env python3

from .app import ConnectionsExtensionApp

def _jupyter_server_extension_points():
    return [{"module": "jupyter_server_connections.app", "app": ConnectionsExtensionApp}]
