import os
import http.server
import socketserver
import multiprocessing
from http import HTTPStatus

def server(directory):
    PORT = 60407 # GODOT

    class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()

        def do_OPTIONS(self):
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()

    Handler = MyHTTPRequestHandler

    os.chdir(directory)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Godot serving at port {PORT}")
        httpd.serve_forever()

def run():
    directory = "godot/ETS2LA-Visualisation/Web Export/"
    multiprocessing.Process(target=server, args=(directory,), daemon=True).start()