
import pytest
import threading
import socket
import time
import requests
from werkzeug.serving import make_server
from app import create_app  

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

@pytest.fixture(scope="session")
def base_url():
    return f"http://127.0.0.1:{get_free_port()}"

@pytest.fixture(scope="session", autouse=True)
def live_server(base_url):

    port = int(base_url.split(":")[-1])
    app = create_app()
    app.config.update({"TESTING": True})

    
    server = make_server("127.0.0.1", port, app)
    

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    
    timeout = 30  
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(f"{base_url}/health") 
            break
        except requests.ConnectionError:
            time.sleep(0.5)
    else:
        raise RuntimeError(f"Server failed to start within {timeout} seconds")

    yield base_url
    server.shutdown()
