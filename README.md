# Cloudstorage Client [![CircleCI](https://circleci.com/gh/SFDigitalServices/cloudstorage-client.svg?style=svg)](https://circleci.com/gh/SFDigitalServices/cloudstorage-client) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/cloudstorage-client/badge.svg?branch=master)](https://coveralls.io/github/SFDigitalServices/cloudstorage-client?branch=master)
Client for the cloudstorage microservice, based off the SFDS Microservice platform
* [falcon](https://falconframework.org/): bare-metal Python web API framework 
* [gunicorn](https://gunicorn.org/): Python WSGI HTTP Server for UNIX
* [pytest](https://docs.pytest.org/en/latest/): Python testing tool 
* [pylint](https://www.pylint.org/): code analysis for Python
* [sentry](https://sentry.io/): error tracking tool
* [jsend](https://github.com/omniti-labs/jsend):  a specification for a simple, no-frills, JSON based format for application-level communication

## Requirement
* Python3 
([Mac OS X](https://docs.python-guide.org/starting/install3/osx/) / [Windows](https://www.stuartellis.name/articles/python-development-windows/))
* Pipenv & Virtual Environments ([virtualenv](https://docs.python-guide.org/dev/virtualenvs/#virtualenvironments-ref) / [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/))

## Get started

Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Set ACCESS_KEY environment var and start WSGI Server
> $ pipenv run gunicorn 'service.microservice:start_service()'

Run Pytest
> $ pipenv run python -m pytest

Get code coverage report
> $ pipenv run python -m pytest --cov=service tests/ --cov-fail-under=100

Open with cURL or web browser
> $ curl --header "ACCESS_KEY: 123456" http://127.0.0.1:8000/welcome


## Development 
Auto-reload on code changes
> $ pipenv run gunicorn --reload 'service.microservice:start_service()'

Code coverage command with missing statement line numbers  
> $ pipenv run python -m pytest --cov=service tests/ --cov-report term-missing

Set up git hook scripts with pre-commit
> $ pipenv run pre-commit install


## Continuous integration
* CircleCI builds fail when trying to run coveralls.
    1. Log into coveralls.io to obtain the coverall token for your repo.
    2. Create an environment variable in CircleCI with the name COVERALLS_REPO_TOKEN and the coverall token value.

