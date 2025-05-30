import os
import sys
import django
import webbrowser
from threading import Timer
import socket
from waitress import serve
from music_recommender.wsgi import application
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static helper
from django.urls import path # Import path
# from django.views.static import serve as serve_static # Import Django's static file server

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def open_browser(port):
    webbrowser.open(f'http://127.0.0.1:{port}')

if __name__ == '__main__':
    # Set up Django environment if not already configured
    if not settings.configured:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_recommender.settings')
        # Set STATIC_ROOT to the bundle directory for static files when running as executable
        if getattr(sys, 'frozen', False): # Check if running as a PyInstaller executable
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            settings.STATIC_ROOT = os.path.join(bundle_dir, 'static')
        
        django.setup()

    # Find a free port
    port = find_free_port()
    
    # Open browser after a short delay, passing the found port
    Timer(1.5, open_browser, args=[port]).start()
    
    # Run the application using Waitress
    print(f"Starting server on http://127.0.0.1:{port}/")
    serve(application, host='127.0.0.1', port=port) 