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

Simply import the adapter and mount it

```python
import requests
from requests_lsp import LSPAdapter

session = requests.Session()
session.mount("lsp://", LSPAdapter())

response = session.get("lsp://127.0.0.1:9084", json={"method": "initialize"})
print(response)
```

## Running tests

Tests are implemented with pytest. To run tests, just do

    pytest tests/

## Release history

 * 0.1
   * Initial release
