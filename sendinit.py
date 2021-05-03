import requests
from requests_lsp import LSPAdapter

with requests.Session() as session:
    session.mount("lsp://", LSPAdapter(debug=True))

    response = session.get("lsp://127.0.0.1:9084", json={"id": "1", "method": "initialize"})
    print(response.json())
