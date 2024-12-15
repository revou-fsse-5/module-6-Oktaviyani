import sys
import os
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Import your Flask app after fixing the path

@pytest.fixture
def client():
    # Set up the Flask test client
    app.testing = True
    with app.test_client() as client:
        yield client  # This is what you use to make requests in tests
