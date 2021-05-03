# requests-lsp

This package provides an adapter for debugging
[Language Server Protocol](https://microsoft.github.io/language-server-protocol/specifications/specification-current/#baseProtocol)
with [requests](http://docs.python-requests.org/en/master/).

The protocol is a JSON-RPC 2.0 with added `Content-Length` header.

The project is a fork of https://github.com/paivett/requests-curl by
@paivett but since then it shares a litle with it, and uses raw sockets
for communication insted of `PyCURL`.

## Installation

Examples may run well without installation, but just in case - clone this
project and run

    python setup.py install

## Usage

Import the adapter, mount it and use `requests.get` to send JSON to LSP
server.

```python
import requests
from requests_lsp import LSPAdapter

with requests.Session() as session:
    session.mount("lsp://", LSPAdapter())

    response = session.get("lsp://127.0.0.1:9084", json={"id": "1", "method": "initialize"})
    print(response.json())
```

The example is in `sendfile.py` file in repository, tested with
Solargraph Ruby LSP server. Use `runserver.sh` script with `podman`
to run it in debug mode for experiments.

On successful request you will see the server capabilities reply, and
this output in Solargraph logs.
```
Solargraph is listening PORT=7658 PID=13
[ANY] Solargraph initialized (2.6497000362724066e-05 seconds)
```

## Running tests

There are no LSP tests for now. There were files from `requests-curl`, which
uses `pytest` for testing.

    pytest tests/

## Release history

 * 0.1
   * Initial release
