# requests-lsp

This package provides an adapter for debugging Language Server Protocol
with [requests](http://docs.python-requests.org/en/master/).

The protocol is a JSON-RPC 2.0 with added `Content-Length` header.

This is a fork of https://github.com/paivett/requests-curl by @paivett.

## Installation

Clone this project, and then, in the desired virtualenvironment, just run

    python setup.py install

[PyPI](https://pypi.org) integration comming soon.

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

## Running tests

There are no LSP tests, only files left from `requests-curl`. Use `pytest` to
run them, and ensure that they properly fail.

    pytest tests/

## Release history

 * 0.1
   * Initial release
