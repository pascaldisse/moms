#!/usr/bin/env python3
"""
Simple BIK to MP4 streaming server using only Python standard library
"""

import os
import subprocess
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import threading
import time

PORT = 8002

class BIKHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/status':
            self.send_json_response({'status': 'running', 'service': 'bik-proxy'})
        elif self.path == '/test-ffmpeg':
            self.test_ffmpeg()
        elif self.path == '/list-bik-files':
            self.list_bik_files()
        elif self.path.startswith('/stream/'):
            self.stream_bik()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/proxy-url':
            self.get_proxy_url()
        else:
            self.send_error(404, "Not Found")
    
    def test_ffmpeg(self):
        """Test if FFmpeg is available"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            response = {
                'status': 'ok' if result.returncode == 0 else 'error',
                'ffmpeg_available': result.returncode == 0,
                'version': result.stdout.split('\n')[0] if result.returncode == 0 else result.stderr
            }
        except FileNotFoundError:
            response = {
                'status': 'error',
                'ffmpeg_available': False,
                'error': 'FFmpeg not found in PATH'
            }
        
        self.send_json_response(response)
    
    def list_bik_files(self):
        """List available BIK files"""
        bik_files = []
        base_path = '/Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN'
        
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith('.bik'):
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, base_path)
                    bik_files.append({
                        'name': file,
                        'path': full_path,
                        'relative_path': relative_path,
                        'size': os.path.getsize(full_path)
                    })
        
        self.send_json_response({'files': bik_files, 'count': len(bik_files)})
    
    def get_proxy_url(self):
        """Generate proxy URL for BIK file"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data)
            file_path = data.get('path', '')
            
            if file_path == 'test':
                self.send_json_response({'status': 'ok', 'message': 'Proxy server is running'})
                return
            
            if not file_path:
                self.send_error(400, "No file path provided")
                return
            
            filename = os.path.basename(file_path)
            proxy_url = f'http://localhost:{PORT}/stream/{filename}?path={file_path}'
            
            self.send_json_response({'url': proxy_url})
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
    
    def stream_bik(self):
        """Stream BIK file as MP4"""
        # Parse the path and query string
        parsed = urlparse(self.path)
        filename = parsed.path.split('/stream/')[-1]
        query_params = parse_qs(parsed.query)
        bik_path = query_params.get('path', [''])[0]
        
        if not bik_path:
            self.send_error(400, "No path provided")
            return
        
        # Find the actual file path
        if not os.path.exists(bik_path):
            possible_paths = [
                bik_path,
                os.path.join('/Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN', bik_path),
                os.path.join('/Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN', 'resource/Bink', filename),
                os.path.join('/Users/pascaldisse/Sync/SOE_Matrix_Online_Win_EN', 'cinematics', filename)
            ]
            
            actual_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    actual_path = path
                    break
            
            if not actual_path:
                self.send_error(404, f"File not found: {bik_path}")
                return
        else:
            actual_path = bik_path
        
        print(f"Streaming BIK file: {actual_path}")
        
        # FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', actual_path,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-c:a', 'aac',
            '-movflags', 'frag_keyframe+empty_moov+faststart',
            '-f', 'mp4',
            '-loglevel', 'warning',  # Reduce FFmpeg verbosity
            'pipe:1'
        ]
        
        # Start FFmpeg process
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Send response headers
        self.send_response(200)
        self.send_header('Content-Type', 'video/mp4')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        # Stream the output
        try:
            bytes_sent = 0
            while True:
                chunk = proc.stdout.read(4096)
                if not chunk:
                    break
                self.wfile.write(chunk)
                bytes_sent += len(chunk)
                if bytes_sent % (1024 * 100) < 4096:  # Log every ~100KB
                    print(f"Streamed {bytes_sent / 1024:.1f} KB")
            
            print(f"Streaming complete. Total: {bytes_sent / 1024:.1f} KB")
            
            # Check for FFmpeg errors
            proc.wait()
            if proc.returncode != 0:
                stderr_output = proc.stderr.read().decode('utf-8', errors='ignore')
                print(f"FFmpeg error (code {proc.returncode}): {stderr_output}")
                
        except BrokenPipeError:
            print("Client disconnected")
        except Exception as e:
            print(f"Streaming error: {e}")
        finally:
            proc.terminate()
            proc.wait()
    
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        response = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Handle requests in separate threads"""
    allow_reuse_address = True

if __name__ == '__main__':
    print(f"Simple BIK Proxy Server starting on http://localhost:{PORT}")
    print("This server streams BIK files as MP4 in real-time")
    print("Available endpoints:")
    print("  POST /proxy-url - Get streaming URL for a BIK file")
    print("  GET /stream/<filename> - Stream BIK as MP4")
    print("  GET /list-bik-files - List available BIK files")
    print("  GET /test-ffmpeg - Test FFmpeg availability")
    
    with ThreadedTCPServer(("", PORT), BIKHandler) as httpd:
        print(f"Server listening on port {PORT}")
        httpd.serve_forever()