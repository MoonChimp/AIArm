#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Nexus AI Direct Server
A simple server that serves the Nexus AI Direct interface
"""

import os
import sys
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow requests from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
        
    def do_OPTIONS(self):
        # Handle OPTIONS request for CORS preflight
        self.send_response(200)
        self.end_headers()

def main():
    """Main function"""
    print("===================================================================== ")
    print("NEXUS AI DIRECT - SERVER")
    print("===================================================================== ")
    
    # Change to the WebInterface directory
    os.chdir(Path("D:/AIArm/WebInterface"))
    
    # Create the server
    handler = CustomHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    
    print(f"Server started at http://localhost:{PORT}")
    print(f"Open your browser and navigate to http://localhost:{PORT}/nexus_direct.html")
    print("Press Ctrl+C to stop the server")
    
    # Open the browser
    webbrowser.open(f"http://localhost:{PORT}/nexus_direct.html")
    
    # Start the server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()
        return 0

if __name__ == "__main__":
    sys.exit(main())
