"""
Host docs on local notework
"""

import os
import sys
import socket
import subprocess
import http.server
import socketserver
from pathlib import Path

def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a socket and connect to an external server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def build_docs():
    """Build the Sphinx documentation."""
    print("Building documentation...")

    if not os.path.exists("source/conf.py"):
        print("Make sure you're running this command from project root.")
        return False
    
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(["sphinx-build", "-b", "html", ".", "_build/html"],
                                 capture_output=True, text=True)
        else:  # Unix-like systems
            result = subprocess.run(["make", "html"],
                                 capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Error building documentation:")
            print(result.stderr)
            return False
            
        return True
        
    except FileNotFoundError:
        print("Error: Make sure you have Sphinx installed:")
        print("pip install sphinx sphinx-rtd-theme")
        return False
    except Exception as e:
        print(f"Error building documentation: {str(e)}")
        return False

def serve_docs(port=8000):
    """Serve the documentation on the specified port."""
    build_dir = Path("build/html")
    if not build_dir.exists():
        print("Error: Built documentation not found.")
        return
    
    ip = get_local_ip()
    
    # Create custom handler to serve from build/html
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(build_dir), **kwargs)
    
    try:
        # Try the specified port
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print("\nServing documentation at:")
            print(f"Local URL:     http://localhost:{port}")
            print(f"Network URL:   http://{ip}:{port}")
            print("\nShare the Network URL with reviewers on your local network.")
            print("\nPress Ctrl+C to stop the server")
            httpd.serve_forever()
    except OSError:
        # If port is in use, try the next one
        print(f"Port {port} is in use, trying {port + 1}...")
        serve_docs(port + 1)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Error serving documentation: {str(e)}")


if __name__ == "__main__":
    if build_docs():
        serve_docs()