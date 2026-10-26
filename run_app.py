"""
Quickstart Launcher for EV Market Analytics Platform
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "web_app"))

from app import app

if __name__ == "__main__":
    print("=" * 60)
    print("   ⚡ Global Electric Vehicle Market Analytics Platform ⚡   ")
    print("=" * 60)
    print("Starting Flask Web Application on http://127.0.0.1:5000 ...")
    print("Open your web browser at: http://127.0.0.1:5000")
    print("Press Ctrl+C in this terminal to stop the server.")
    print("=" * 60)
    
    app.run(host="127.0.0.1", port=5000, debug=True)
