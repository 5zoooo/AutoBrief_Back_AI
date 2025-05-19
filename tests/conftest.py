# conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
import os

@pytest.fixture(scope="module")
def test_app():
    # Set up test environment
    test_upload_dir = "./test_uploads"
    os.makedirs(test_upload_dir, exist_ok=True)
    
    # Override settings for testing
    settings.UPLOAD_FOLDER = test_upload_dir
    settings.DEBUG = True
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up after tests
    import shutil
    if os.path.exists(test_upload_dir):
        shutil.rmtree(test_upload_dir)

@pytest.fixture
def test_audio_file():
    # Create a dummy audio file for testing
    test_file = "test_audio.mp3"
    with open(test_file, "wb") as f:
        f.write(b"dummy audio content")
    yield test_file
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
