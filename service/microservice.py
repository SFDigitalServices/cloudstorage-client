"""Main application module"""
import os
from urllib import parse
import sentry_sdk
import falcon
import requests

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
    parsed = parse.urlparse(_req.uri)

    # strip off leading /
    path = parsed.path[1:]

    # determine whether to use amazon s3 or azure blob storage
    # Use 'az' at beginning of the path to signal that file is from azure
    # eg. https://domain.com/az/some_file.pdf
    microservice_url = os.environ.get('CLOUDSTORAGE_URL') # default to s3

    request_params = {
        'name':path,
        'apikey':os.environ.get('CLOUDSTORAGE_API_KEY')
    }

    if path[0:3] == 'az/':
        microservice_url = microservice_url.replace('1.0', '2.0', 1)
        request_params['name'] = path[3:]  # remove az from name

        # pass thru querystring
        parsed_query_dict = parse.parse_qs(parsed.query)
        for param, val in parsed_query_dict.items():
            request_params[param] = val[0]

    response = requests.get(
        microservice_url,
        params=request_params,
        timeout=300
    )
    resp.status = falcon.get_http_status(response.status_code)
    resp.content_type = response.headers['Content-Type']
    resp.body = response.content
