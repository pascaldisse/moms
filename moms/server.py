#!/usr/bin/env python3
"""
Simple HTTP server for the Matrix Online Modding Suite
Serves files with proper CORS headers to avoid browser restrictions
"""

import http.server
import socketserver
import os

PORT = 8000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print(f"Serving directory: {os.getcwd()}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()