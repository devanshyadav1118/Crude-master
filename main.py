import os
import socket
import mimetypes

class TCPServer:
    """Base server class for handling TCP connections.
    The HTTP server will inherit from this class.
    """
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        """Method for starting the server"""
        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow reuse of the address to avoid "Address already in use" errors
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind the socket to the specified host and port
        s.bind((self.host, self.port))
        # Listen for incoming connections, with a backlog queue of 5
        s.listen(5)
        while True:
            # Accept a connection from a client
            conn, addr = s.accept()
            # Receive data from the client (limited to 1024 bytes for this example)
            data = conn.recv(1024)
            # Handle the request and generate a response
            response = self.handle_request(data)
            # Send the response back to the client
            conn.sendall(response)
            # Close the connection
            conn.close()

    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data

class HTTPServer(TCPServer):
    """The actual HTTP server class."""
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }
    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def handle_request(self, data):
        """Handles incoming requests"""
        # Parse the HTTP request
        request = HTTPRequest(data)
        try:
            # Find the appropriate handler method for the request method
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            # Use the default handler for unimplemented methods
            handler = self.HTTP_501_handler
        # Call the handler and generate a response
        response = handler(request)
        return response

    def response_line(self, status_code):
        """Returns response line (as bytes)"""
        reason = self.status_codes[status_code]
        response_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)
        return response_line.encode()

    def response_headers(self, extra_headers=None):
        """Returns headers (as bytes).
        The `extra_headers` can be a dict for sending
        extra headers with the current response
        """
        headers_copy = self.headers.copy()
        if extra_headers:
            headers_copy.update(extra_headers)
        headers = ''
        for h in headers_copy:
            headers += '%s: %s\r\n' % (h, headers_copy[h])
        return headers.encode()

    def handle_OPTIONS(self, request):
        """Handler for OPTIONS HTTP method"""
        response_line = self.response_line(200)
        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)
        blank_line = b'\r\n'
        return b''.join([response_line, response_headers, blank_line])

    def handle_GET(self, request):
        """Handler for GET HTTP method"""
        # Extract the path from the URI and handle various cases
        path = request.uri.strip('/')
        if not path:
            path = 'index.html'
        if os.path.exists(path) and not os.path.isdir(path):
            # Serve the requested file if it exists
            response_line = self.response_line(200)
            content_type = mimetypes.guess_type(path)[0] or 'text/html'
            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)
            with open(path, 'rb') as f:
                response_body = f.read()
        else:
            # Respond with a 404 error if the file is not found
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b'<h1>404 Not Found</h1>'
        blank_line = b'\r\n'
        # Combine the response components into a single byte string
        response = b''.join([response_line, response_headers, blank_line, response_body])
        return response

    def HTTP_501_handler(self, request):
        """Returns 501 HTTP response if the requested method hasn't been implemented."""
        response_line = self.response_line(status_code=501)
        response_headers = self.response_headers()
        blank_line = b'\r\n'
        response_body = b'<h1>501 Not Implemented</h1>'
        return b"".join([response_line, response_headers, blank_line, response_body])

class HTTPRequest:
    """Parser for HTTP requests.
    It takes raw data and extracts meaningful information about the incoming request.
    Instances of this class have the following attributes:
        self.method: The current HTTP request method sent by client (string)
        self.uri: URI for the current request (string)
        self.http_version = HTTP version used by  the client (string)
    """
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1'
        self.parse(data)

    def parse(self, data):
        lines = data.split(b'\r\n')
        request_line = lines[0]
        words = request_line.split(b' ')
        self.method = words[0].decode()
        if len(words) > 1:
            self.uri = words[1].decode()
        if len(words) > 2:
            self.http_version = words[2]


if __name__ == '__main__':
    server = HTTPServer()
    server.start()



