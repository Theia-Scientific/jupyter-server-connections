#!/usr/bin/env python3

from jupyter_server.extension.application import ExtensionApp

from .handlers import DefaultHandler

class ConnectionsExtensionApp(ExtensionApp):
    name = "jupyter_server_connections"
    extension_url = "/jupyter_server_connetions/default"
    local_other_extensions = False
    file_url_prefix = "/render"

    def initialize_handlers(self):
        self.handlers.extend([
            (rf"/connections", DefaultHandler)
        ])

    def initialize_settings(self):
        self.log.info("Initialize settings")

main = launch_new_instance = ConnectionsExtensionApp.launch_instance
