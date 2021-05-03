import requests
from requests_lsp import LSPAdapter

with requests.Session() as session:
    session.mount("lsp://", LSPAdapter(debug=True))

    ls = "lsp://127.0.0.1:9084"
    response = session.get(ls, json={"id": "1", "method": "initialize"})
    print(response.json())

    resp = session.get(ls, json={"id": "2", "method": "initialized"})
    print(resp.json())
