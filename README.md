# Crude Server: A Simple Python HTTP Server 

This is a simple HTTP server implementation in Python designed for educational purposes. It demonstrates the core concepts of building a basic, functional HTTP server from scratch.

**Features**

* Handles HTTP GET and OPTIONS methods.
* Serves static files (HTML, CSS, JavaScript).
* Supports basic MIME type detection.
* Includes error handling (404 Not Found, 501 Not Implemented).

**Usage**

1. **Prerequisites:**
   - Python (https://www.python.org/)

2. **Get the code:**
   - Clone or download this repository. 

3. **Run the server:**
   - `python server.py`

**Getting Started**

* **TCPServer Class:** Foundation for handling TCP connections, establishes listening and delegation of requests.
* **HTTPServer Class:** Subclass of TCPServer, implements the core HTTP server logic for handling requests.
* **HTTPRequest Class:**  Used to parse incoming HTTP requests to identify the method, URI, etc.

**Customization**

* Extend the `HTTPServer` class and add methods to handle additional HTTP methods.
* Change the `headers` dictionary within the `HTTPServer` class for custom response headers.

**Contributing**

We appreciate your contributions! Please report issues or create pull requests on GitHub.
 
 
