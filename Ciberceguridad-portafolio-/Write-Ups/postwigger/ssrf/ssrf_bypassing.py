from http.server import HTTPServer, BaseHTTPRequestHandler

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', 'http://127.0.0.1/admin')
        self.end_headers()

HTTPServer(('0.0.0.0', 8000), RedirectHandler).serve_forever()
