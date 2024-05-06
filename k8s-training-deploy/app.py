#!/usr/bin/env python3
# coding: utf-8

import os
import signal
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        version = os.environ.get('VERSION', 'v0')
        hostname = socket.gethostname()
        if version == "v1":
          version = "v1 *🔵 🔵 *"
        elif version == "v2":
          version = "v2       #🟩 🟩 #"
        message = 'Hello from {} and version {}\n'.format(hostname, version)
        self.wfile.write(bytes(message, 'utf8'))


def run():
    host = '0.0.0.0'
    port = 8080
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server is listening on http://{}:{}'.format(host, port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print('Stopped')


signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
run()
