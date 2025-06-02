#!/usr/bin/env python3
"""
Matrix Online Modding Suite API Server
Provides API endpoints for file browsing, video conversion, and packet analysis
"""

import http.server
import socketserver
import json
import os
import urllib.parse
import mimetypes
import subprocess
import hashlib
from pathlib import Path
import threading
import time

PORT = 8000
CACHE_DIR = "cache"

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)

class APIHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # Serve static files
        if not path.startswith('/api/'):
            if path == '/':
                path = '/index.html'
            self.serve_static_file(path[1:])  # Remove leading slash
            return
        
        # Handle API endpoints
        if path == '/api/status':
            self.handle_status()
        elif path == '/api/files':
            self.handle_files(query)
        elif path == '/api/file':
            self.handle_file_content(query)
        else:
            self.send_error(404, "API endpoint not found")
    
    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Read POST data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data) if content_length > 0 else {}
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        # Handle API endpoints
        if path == '/api/convert-bik':
            self.handle_convert_bik(data)
        elif path == '/api/parse-packet':
            self.handle_parse_packet(data)
        else:
            self.send_error(404, "API endpoint not found")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def serve_static_file(self, path):
        """Serve static files with proper content types"""
        try:
            # Security: prevent directory traversal
            safe_path = os.path.normpath(path)
            if safe_path.startswith('..') or os.path.isabs(safe_path):
                self.send_error(403, "Forbidden")
                return
            
            if not os.path.exists(safe_path):
                self.send_error(404, "File not found")
                return
            
            # Guess content type
            content_type, _ = mimetypes.guess_type(safe_path)
            if not content_type:
                content_type = 'application/octet-stream'
            
            # Send file
            with open(safe_path, 'rb') as f:
                content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(content)))
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Internal error: {str(e)}")
    
    def handle_status(self):
        """Return server status"""
        status = {
            "status": "running",
            "version": "1.0",
            "uptime": int(time.time() - server_start_time)
        }
        self.send_json_response(status)
    
    def handle_files(self, query):
        """List files in a directory"""
        path = query.get('path', ['/'])[0]
        
        # For demo purposes, return mock data
        # In a real implementation, you would list actual files
        files = []
        
        if path == '/':
            # Root directory - show some example folders
            files = [
                {"name": "cinematics", "type": "directory", "path": "/cinematics"},
                {"name": "recordings", "type": "directory", "path": "/recordings"},
                {"name": "packets", "type": "directory", "path": "/packets"},
                {"name": "test.bik", "type": "file", "path": "/test.bik", "size": 1048576},
                {"name": "combat.rec", "type": "file", "path": "/combat.rec", "size": 524288}
            ]
        elif path == '/cinematics':
            files = [
                {"name": "intro.bik", "type": "file", "path": "/cinematics/intro.bik", "size": 10485760},
                {"name": "outro.bik", "type": "file", "path": "/cinematics/outro.bik", "size": 8388608},
                {"name": "cutscene1.bik", "type": "file", "path": "/cinematics/cutscene1.bik", "size": 5242880}
            ]
        elif path == '/recordings':
            files = [
                {"name": "session1.rec", "type": "file", "path": "/recordings/session1.rec", "size": 2097152},
                {"name": "session2.rec", "type": "file", "path": "/recordings/session2.rec", "size": 3145728}
            ]
        
        response = {"files": files, "path": path}
        self.send_json_response(response)
    
    def handle_file_content(self, query):
        """Serve file content"""
        path = query.get('path', [''])[0]
        
        # For demo purposes, return a placeholder
        self.send_response(200)
        self.send_header('Content-Type', 'application/octet-stream')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(b"File content placeholder")
    
    def handle_convert_bik(self, data):
        """Handle BIK to MP4 conversion request"""
        bik_path = data.get('path', '')
        
        # Generate cache key
        cache_key = hashlib.md5(bik_path.encode()).hexdigest()
        mp4_filename = f"{cache_key}.mp4"
        
        # Return mock response
        response = {
            "success": True,
            "url": f"/cache/{mp4_filename}",
            "message": "BIK file queued for conversion"
        }
        self.send_json_response(response)
    
    def handle_parse_packet(self, data):
        """Parse a Matrix Online packet"""
        hex_data = data.get('hex', '')
        
        # Mock packet parsing
        parsed = {
            "type": "POSITION_UPDATE",
            "size": len(hex_data) // 2,
            "data": {
                "x": 100.5,
                "y": 50.0,
                "z": 200.75,
                "rotation": 180.0
            }
        }
        self.send_json_response(parsed)
    
    def send_json_response(self, data):
        """Send JSON response with proper headers"""
        content = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(content)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(content)
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}")

# Track server start time
server_start_time = time.time()

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the server
with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
    print(f"Matrix Online Modding Suite API Server")
    print(f"Running at http://localhost:{PORT}")
    print(f"Serving directory: {os.getcwd()}")
    print("Press Ctrl+C to stop")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()