"""Main application module"""
import os
from urllib.parse import urlparse
import sentry_sdk
import falcon
import requests

CLOUDSTORAGE_URL = os.environ.get('CLOUDSTORAGE_URL')
CLOUDSTORAGE_API_KEY = os.environ.get('CLOUDSTORAGE_API_KEY')

def start_service():
    """Start this service
    set SENTRY_DSN environmental variable to enable logging with Sentry
    """
    # Initialize Sentry
    sentry_sdk.init(os.environ.get('SENTRY_DSN'))
    # Initialize Falcon
    api = falcon.API()
    api.add_sink(cloud_storage_service, '')
    return api

def cloud_storage_service(_req, resp):
    """Send the request through to the cloudstorage microservice"""
    path = urlparse(_req.uri).path[1:]
    response = requests.get(
        CLOUDSTORAGE_URL,
        params={
            'name':path,
            'apikey':CLOUDSTORAGE_API_KEY
        }
    )
    resp.status = falcon.get_http_status(response.status_code)
    resp.content_type = response.headers['Content-Type']
    resp.body = response.content
