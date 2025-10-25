#!/usr/bin/env python
"""
Simple HTTP server for LIRA UI
Serves the interface on port 8080
"""
import http.server
import socketserver
import os
from pathlib import Path

# Change to LIRA UI directory
os.chdir(Path(__file__).parent)

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("=" * 60)
    print("NEXUS-LIRA Web Interface Server")
    print("=" * 60)
    print(f"Serving at: http://localhost:{PORT}")
    print(f"Directory: {os.getcwd()}")
    print("")
    print("Open in browser: http://localhost:8080")
    print("=" * 60)
    httpd.serve_forever()
