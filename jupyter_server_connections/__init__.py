#!/usr/bin/env python3

from typing import Any, Dict, List

from .app import ConnectionsExtensionApp


def _jupyter_server_extension_points() -> List[Dict[str, Any]]:  # pragma: no cover
    return [{"module": "jupyter_server_connections.app", "app": ConnectionsExtensionApp}]
