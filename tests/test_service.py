# pylint: disable=redefined-outer-name
"""Tests for microservice"""
import os
from unittest.mock import patch
import pytest
from falcon import testing
import service.microservice

ENV_VARS = {
    "CLOUDSTORAGE_URL": "https://endpoint.api.com",
    "CLOUDSTORAGE_API_KEY": "1234567"
}

FILES_PATH = 'tests/resources/'

@pytest.fixture()
def client():
    """ client fixture """
    return testing.TestClient(app=service.microservice.start_service())

@pytest.fixture
def mock_env(monkeypatch):
    """ mock environment var """
    for key in ENV_VARS:
        monkeypatch.setenv(key, ENV_VARS[key])

def test_endpoint(client, mock_env):
    # pylint: disable=unused-argument
    """Test the endpoint"""

    with patch('service.microservice.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.headers = {'Content-Type':'application/pdf'}
        with open(os.path.join(FILES_PATH, 'dummy.pdf'), 'rb') as f: # pylint: disable=invalid-name
            content = f.read()
            mock_get.return_value.content = content

            # pdf happy path amazon s3
            response = client.simulate_get('/dummy.pdf')
            assert response.status_code == 200
            assert response.headers['Content-Type'] == 'application/pdf'
            assert response.content == content

            # happy path azure blob storage
            response = client.simulate_get('/az/dummy.pdf')
            assert response.status_code == 200
            assert response.headers['Content-Type'] == 'application/pdf'
            assert response.content == content

    # 404 file not found
    with patch('service.microservice.requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.content = "File not found"

        response = client.simulate_get('/file_that_no_exists')
        assert response.status_code == 404
