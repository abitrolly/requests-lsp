"""Requests adapter implementing a JSON-RPC protocol for LSP"""

from requests import Response
from requests.adapters import BaseAdapter
from urllib3.util import parse_url, connection


def debug_on():
    # Turn on requests logging (which still doesn't log response body)
    # https://docs.python-requests.org/en/master/api/#api-changes
    import logging

    # Enabling debugging at http.client level (requests->urllib3->http.client)
    # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with
    # HEADERS but without DATA.
    #
    # The only thing missing will be the response.body which is not logged.
    try:  # for Python 3
        from http.client import HTTPConnection
    except ImportError:
        from httplib import HTTPConnection
    HTTPConnection.debuglevel = 1

    logging.basicConfig()  # initialize logging, otherwise you will not see anything from requests
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    # Log request body manually
    #
    # import requests
    # resp = requests.post('https://httpbin.org/post', json={"method": "initialize"})
    # print(resp.text)


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

        # store connections as "host:port" -> connection
        self._connections = {}

        if debug:
            self.debug = True
            # httplib is unused, but in case it somehow fires..
            debug_on()

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

        self.debug = True
        if self.debug:
            for line in output:
                print('> ' + line.decode('utf-8'))

        conn.sendall(b'\r\n'.join(output))

        response = Response()
        response.request = request
        with conn.makefile('rb') as fs:
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

        return response

    def close(self):
        """Cleans up adapter specific items."""
        for _, conn in self._connections.items():
            conn.close()
        self._connections = {}
