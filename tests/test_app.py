#!/usr/bin/env python3

import json
import pytest
import urllib.parse

from jupyter_server.utils import url_path_join
from tornado.escape import url_escape

@pytest.fixture
def jsc_serverapp(jp_configurable_serverapp):
    return jp_configurable_serverapp(config={
        "ServerApp": {
            "jpserver_extensions": {"jupyter_server_terminals": True, "jupyter_server_connections": True}
        }
    })

@pytest.fixture
def jsc_fetch(jsc_serverapp, http_server_client, jp_auth_header, jp_base_url):
    _ = jsc_serverapp

    def client_fetch(*parts, headers=None, params=None, **kwargs):
        if not headers:
            headers = {}
        if not params:
            params = {}
        path_url = url_escape(url_path_join(*parts), plus=False)
        base_path_url = url_path_join(jp_base_url, path_url)
        params_url = urllib.parse.urlencode(params)
        url = base_path_url + "?" + params_url
        for key, value in jp_auth_header.items():
            headers.setdefault(key, value)
        request_timeout = kwargs.pop("request_timeout", 20)
        return http_server_client.fetch(
            url, headers=headers, request_timeout=request_timeout, **kwargs
        )
    return client_fetch

async def test_kernel_connection(jsc_fetch):
    # Confirm there are no kernels
    response = await jsc_fetch("api", "kernels", method="GET")
    assert response.code == 200
    data = json.loads(response.body)
    assert len(data) == 0

    # Create a new kernel
    response = await jsc_fetch("api", "kernels", method="POST", body="{}")
    assert response.code == 201
    kernel = json.loads(response.body)
    assert "id" in kernel
    assert "name" in kernel
    assert "last_activity" in kernel
    assert "execution_state" in kernel
    assert "connections" in kernel
    kernel_id = kernel["id"]
    assert kernel_id is not None
    kernel_name = kernel["name"]
    assert kernel_name is not None

    # Get the connection file
    response = await jsc_fetch("api", "kernels", kernel_id, "connection", method="GET")
    assert response.code == 200
    kernel_conn = json.loads(response.body)
    assert "shell_port" in kernel_conn
    assert "iopub_port" in kernel_conn
    assert "stdin_port" in kernel_conn
    assert "control_port" in kernel_conn
    assert "hb_port" in kernel_conn
    assert "ip" in kernel_conn
    assert "key" in kernel_conn
    assert "transport" in kernel_conn
    assert "signature_scheme" in kernel_conn
    assert "kernel_name" in kernel_conn
    assert 1024 < kernel_conn["shell_port"] < 65535
    assert 1024 < kernel_conn["iopub_port"] < 65535
    assert 1024 < kernel_conn["stdin_port"] < 65535
    assert 1024 < kernel_conn["control_port"] < 65535
    assert 1024 < kernel_conn["hb_port"] < 65535
    assert kernel_conn["ip"] == "127.0.0.1"
    assert kernel_conn["key"] is not None
    assert kernel_conn["transport"] == "tcp"
    assert kernel_conn["kernel_name"] == kernel_name
