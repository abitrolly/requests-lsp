"""Requests adapter implementing a JSON-RPC protocol for LSP"""

from requests import Response
from requests.adapters import BaseAdapter
from urllib3.util import parse_url, connection


class LSPAdapter(BaseAdapter):
    """
    A requests adapter for JSON-RPC used in LSP.

    Uses urllib3 helpers for connecting and parsing urls.
    """

    debug = False

    def __init__(self, debug=False):
        """
        Args:
            debug (bool): if set, prints sent and received data.
        """
        super(LSPAdapter, self).__init__()
        self.debug = debug

        # store connections as "host:port" -> connection
        self._connections = {}

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):
        """Sends PreparedRequest object. Returns Response object.

        Args:
            request (PreparedRequest): the request being sent.
            stream (bool, optional): unused
            timeout (float, optional): unused
            verify (bool, optional): unused
            cert (str, optional): unused
            proxies (dict,  optional): unused

        Returns:
            request.Response: the response to the request.
        """

        # https://docs.python-requests.org/en/master/api/#requests.PreparedRequest

        # Connect to LSP server using raw socket
        purl = parse_url(request.url)
        hostport = purl.host + ':' + str(purl.port)
        conn = self._connections.get(hostport, None)
        if not conn:
            conn = connection.create_connection([purl.host, purl.port])
            self._connections[hostport] = conn

        # Calculate header block with Content-length
        header = 'Content-Length: ' + str(len(request.body))

        output = []
        # encode everything into bytes
        output.append(header.encode())
        output.append(b'')
        # add body
        output.append(request.body)

        if self.debug:
            for line in output:
                print('> ' + line.decode('utf-8'))

        conn.sendall(b'\r\n'.join(output))

        # Parse response
        response = Response()
        response.request = request

        # [ ] if "id" is not specified, the read will hang
        #     so don't read if no "id" in initial JSON

        fs = conn.makefile('rb')
        # read Content-Length header
        header = fs.readline()
        if self.debug:
            print('< ' + header.strip().decode('utf-8'))
        line = fs.readline()
        if self.debug:
            print('< ' + line.strip().decode('utf-8'))
        readlen = int(header.split()[1])
        response.headers['Content-Length'] = readlen
        body = fs.read(readlen)
        if self.debug:
            print('< ' + body.decode('utf-8'))
        response._content = body
        fs.close()

        return response

    def close(self):
        """Cleans up adapter specific items."""
        for _, conn in self._connections.items():
            conn.close()
        self._connections = {}
