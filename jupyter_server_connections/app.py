#!/usr/bin/env python3

from jupyter_server.extension.application import ExtensionApp
from jupyter_server.services.kernels.handlers import _kernel_id_regex

from .handlers import KernelConnectionHandler

class ConnectionsExtensionApp(ExtensionApp):
    name = "jupyter_server_connections"
    extension_url = "/connetions"
    local_other_extensions = False

    def initialize_handlers(self):
        self.handlers.extend([
            (r"/kernels/%s/connection" % _kernel_id_regex, KernelConnectionHandler)
        ])

    def initialize_settings(self):
        self.log.info("Initialize settings")

main = launch_new_instance = ConnectionsExtensionApp.launch_instance
