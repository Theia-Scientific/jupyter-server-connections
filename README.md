# jupyter-server-connections: A Jupyter server extension to share kernel connection files 

[![CI](https://github.com/Theia-Scientific/jupyter-server-connections/workflows/CI/badge.svg)](https://github.com/Theia-Scientific/jupyter-server-connections/actions/workflows/ci.yml)
[![Release](https://github.com/Theia-Scientific/jupyter-server-connections/workflows/Release/badge.svg)](https://github.com/Theia-Scientific/jupyter-server-connections/actions/workflows/release.yml)

Each kernel creates a [connections file] formatted as JSON that contains the
ports used for creating the various [ZeroMQ] sockets to communicate with the
kernel. This file is located in the `JUPYTER_RUNTIME_DIR` directory, e.g.,
`~/.local/share/jupyter/data/runtime`, with a `kernel-<id>.json` file name
structure, where `<id>` is replaced with the UUID of the kernel. The UUID is
automatically generated when using the `POST /kernels` endpoint of the
[jupyter_server REST API].

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

## Installation

1. Obtain a package key from Theia Scientific personnel. Save it for Step 2.
2. Install the `jupyter_server_connections` package using `pip` and the private
   package repository.

   ```sh
   pip install --extra-index-url="https://pypi:<KEY>@app.envelope.dev/simple/" jupyter_server_connections
   ```
   
## Contributing

1. Clone this repository.

   ```sh
   git clone https://github.com/Theia-Scientific/jupyter_server_connections.git && cd jupyter_server_connections
   ```

2. Create a virtual environment.

   ```sh
   python3 -m venv .venv
   ```

3. Activate the virtual environment.

   ```sh
   source .venv/bin/activate
   ```

   or if [direnv] is installed:
   
   ```sh
   cp .envrc.example .envrc
   ```
   
   followed by:
   
   ```sh
   direnv allow
   ```

4. Install the package, utility, the required dependencies, and the development
   dependencies.

   ```sh
   python3 -m pip install -e ".[dev]"
   ```

5. Create a local branch.

   ```sh
   git checkout -b feature-awesome-new-feature
   ```

6. Modify the code.
7. Manually test features by starting the Jupyter server.

   ```sh
   jupyter server --ServerApp.jpserver_extensions="{'jupyter_server_connections': True}"
   ```
  
   Information will be printed to the console, e.g.,
   
   ```sh
   [I 2025-12-13 13:35:01.795 ServerApp] jupyter_server_connections | extension was successfully linked.
   [I 2025-12-13 13:35:01.797 ServerApp] jupyter_server_terminals | extension was successfully linked.
   [I 2025-12-13 13:35:01.810 ConnectionsExtensionApp] Initialize settings
   [I 2025-12-13 13:35:01.810 ServerApp] jupyter_server_connections | extension was successfully loaded.
   [I 2025-12-13 13:35:01.810 ServerApp] jupyter_server_terminals | extension was successfully loaded.
   [I 2025-12-13 13:35:01.812 ServerApp] Serving notebooks from local directory: /home/cfield/Code/jupyter_server_connections
   [I 2025-12-13 13:35:01.812 ServerApp] Jupyter Server 2.17.0 is running at:
   [I 2025-12-13 13:35:01.812 ServerApp] http://localhost:8888/?token=<TOKEN>
   [I 2025-12-13 13:35:01.812 ServerApp]     http://127.0.0.1:8888/?token=<TOKEN>
   [I 2025-12-13 13:35:01.812 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
   [C 2025-12-13 13:35:01.814 ServerApp]
   
       To access the server, open this file in a browser:
           file:///home/cfield/.local/share/jupyter/runtime/jpserver-<ID>-open.html
       Or copy and paste one of these URLs:
           http://localhost:8888/?token=<TOKEN>
           http://127.0.0.1:8888/?token=<TOKEN>
   ```
   
   Copy the `<TOKEN>` value and save for later. It will be needed for executing
   [curl] commands.
   
   Start a new terminal while leaving the previous terminal running, and create
   a shell variable for the `<TOKEN>` value copied earlier from the previous
   terminal still running the `jupyter server` application.
   
   ```sh
   export TOKEN=<TOKEN>
   ```
   
   Check if any kernels already exist.
   
   ```sh
   curl "http://localhost:8888/api/kernels?token=${TOKEN}"
   []
   ```
   
   Create a new kernel. 
   
   ```sh
   curl -X POST -d '{"name":"python3"}' "http://localhost:8888/api/kernels?token=${TOKEN}"
   [{"id": "b2042229-7c6c-416b-9ae2-97ae16017cf5", "name": "python3", "last_activity": "2025-12-13T18:11:28.731478Z", "execution_state": "starting", "connections": 0}]
   ```
   
   Copy the value for the `id` field and export to a shell variable.
   
   ```sh
   export ID=b2042229-7c6c-416b-9ae2-97ae16017cf5
   ```
   
   Try the endpoints from this extension.
   
   ```sh
   $ curl "http://localhost:8888/api/kernels/${ID}/connection?token=${TOKEN}"
   {"shell_port": 42679, "iopub_port": 35375, "stdin_port": 58141, "control_port": 48063, "hb_port": 55541, "ip": "127.0.0.1", "key": "6a553a72-a32a994e0a70400ae68a6922", "transport": "tcp", "signature_scheme": "hmac-sha256", "kernel_name": "python3"}
   ```

   When done testing, close the current terminal that was used to invoke `curl`
   commands. Change back to the terminal running the `jupyter server` command.
   Press `CTRL+C` and enter `Y` to stop the process.

8. Run automated tests locally on developer machine, and add tests to maintain
   100% coverage as needed.

   ```sh
   pytest --color=yes --cov=jupyter_server_connections --cov-report=term-missing
   ```

9. Run linter for style conformity and minimize potential bugs.

   ```sh
   flake8 . --exclude .venv --count --max-complexity=10 --max-line-length=127 --statistics
   ```

10. Commit changes to your local branch.

    ```sh
    git add -A && git commit -m "Add new feature"
    ```

11. Push your local branch to GitHub to create a Pull Request (PR).

    ```sh
    git push origin feature-awesome-new-feature
    ```

12. Create a Pull Request (PR) in GitHub.
13. Wait for CI to complete.
14. Add comment to PR that it is ready to review.

## License

This project is licensed under either the [3-Clause BSD license] See the
[LICENSE] file for information about licensing and copyright.

[3-clause bsd license]: https://opensource.org/license/bsd-3-clause
[connections file]: https://jupyter-client.readthedocs.io/en/stable/kernels.html#connection-files
[curl]: https://curl.se/
[direnv]: https://direnv.net/
[jupyter_server rest api]: https://jupyter-server.readthedocs.io/en/latest/developers/rest-api.html
[license]: https://github.com/Theia-Scientific/jupyter-server-connections/blob/main/LICENSE
[zeromq]: https://zeromq.org/

