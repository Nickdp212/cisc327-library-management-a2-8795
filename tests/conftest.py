# conftest.py
import pytest
import threading
import socket
import time
import requests
from werkzeug.serving import make_server
from app import create_app  # Import your actual app factory

def get_free_port():
    """Find a free port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@pytest.fixture(scope="session")
def base_url():
    """
    Returns the URL where the server is running.
    Pytest-playwright uses this automatically for page.goto()
    """
    return f"http://127.0.0.1:{get_free_port()}"

@pytest.fixture(scope="session", autouse=True)
def live_server(base_url):
    """
    Starts the Flask app in a background thread.
    """
    port = int(base_url.split(":")[-1])
    app = create_app()
    app.config.update({"TESTING": True})

    # Create a robust server instance
    server = make_server("127.0.0.1", port, app)
    
    # Run server in a daemon thread
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # Poll until the server is actually ready (critical for heavy ML apps)
    timeout = 30  # Give it 30 seconds to load models
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(f"{base_url}/health") # or just requests.get(base_url)
            break
        except requests.ConnectionError:
            time.sleep(0.5)
    else:
        raise RuntimeError(f"Server failed to start within {timeout} seconds")

    yield base_url
    
    # Teardown (optional since daemon thread dies with main process)
    server.shutdown()
