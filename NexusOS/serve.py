#!/usr/bin/env python
"""HTTP server for NexusOS interface"""
import http.server
import socketserver
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"NexusOS serving at http://localhost:{PORT}")
    httpd.serve_forever()
