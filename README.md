# jupyter_server_connections: A Jupyter server extension to share kernel connection files 

Each kernel creates a connections file formatted as JSON that contains the ports
used for creating the various ZeroMQ sockets to communicate with the kernel.
This file is located in the `JUPYTER_RUNTIME_DIR` directory, e.g.,
`~/.local/share/jupyter/data/runtime`, with a `kernel-<id>.json` file name
structure, where `<id>` is replaced with the UUID of the kernel. The UUID is
automatically generated when using the `POST /kernels` endpoint of the
JupyterServer REST API.

The `POST /kernels` endpoint returns only the `Location` header to the newly
created kernel. The `GET /kernels` endpoint returns a list of kernels with some
information about the kernels, like the `id`, `name`, `execution_count`, and
`last_activity`. The `GET /kernels/{id}` endpoint of the jupyter_server REST API
returns the same information for a specific kernel. However, the connection file
contents are not supplied by these endpoints. So, a client using the
jupyter_server REST API can create, start, stop, and remove kernels but there is
no way to obtain the connection file contents for the kernels from the
jupyter_server REST API, which is needed to establish a connection to the ZeroMQ
sockets to connect and execute code on the kernels.

I have not found a solution to this. There is probably another extension or tool
I am supposed to use (Gateway?), but this seems like something that should be
provided with the REST API. This extension adds endpoints to the jupyter_server
REST API to get connection files for kernels. This eliminates the need to use
alternative methods to communicate the connection files to clients, such as
Network File System (NFS).
