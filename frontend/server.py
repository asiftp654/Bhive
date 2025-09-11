#!/usr/bin/env python3
"""
Simple HTTP server for serving the Bhive Mutual Fund frontend.
Usage: python server.py [port]
Default port: 8080
"""

import http.server
import socketserver
import sys
import os
import webbrowser
from pathlib import Path

def main():
    # Default port
    PORT = 8080
    
    # Check if port is provided as argument
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8080.")
    
    # Change to the frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Add MIME type for JavaScript files
    Handler.extensions_map.update({
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.html': 'text/html',
    })
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            server_url = f"http://localhost:{PORT}"
            print(" Bhive Mutual Fund Frontend Server")
            print(" Make sure the backend is running at http://localhost:8000")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(" Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {PORT} is already in use. Try a different port:")
            print(f"python server.py {PORT + 1}")
        else:
            print(f" Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
