from http.server import HTTPServer, BaseHTTPRequestHandler

def get_answer(question):
	if question == 'hello':
		return 'world'
	else:
		return 'please ask again'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(get_answer(body.decode('utf-8')).encode('utf-8'))

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()