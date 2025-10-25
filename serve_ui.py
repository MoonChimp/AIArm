#!/usr/bin/env python3
"""
Simple HTTP server to serve the Nexus UI without needing Node.js build tools
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 3002
DIRECTORY = str(Path(__file__).parent / "NexusUI_Static")

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"""
================================================================================
Nexus UI Server Running
================================================================================
Serving at: http://localhost:{PORT}
Directory: {DIRECTORY}
================================================================================
        """)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
