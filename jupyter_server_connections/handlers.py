#!/usr/bin/env python3

import json

from jupyter_client.jsonutil import json_default
from jupyter_client.connect import find_connection_file
from jupyter_server.auth.decorator import authorized
from jupyter_server.base.handlers import JupyterHandler
from tornado import web

AUTH_RESOURCE = "connections"

class ConnectionsHandler(JupyterHandler):

    auth_resource = AUTH_RESOURCE
    
class KernelConnectionHandler(ConnectionsHandler):
    @web.authenticated
    @authorized
    async def get(self, kernel_id):
        connection_file_path = find_connection_file(f"kernel-{kernel_id}.json")
        with open(connection_file_path) as f:
            info = json.load(f)
        self.finish(json.dumps(info, default=json_default))
