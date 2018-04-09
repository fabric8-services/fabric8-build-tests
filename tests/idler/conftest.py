import pytest
import requests
import os

def pytest_addoption(parser):
    parser.addoption("--idler-url", action="store", help="", default="https://idler.openshift.io")
    parser.addoption("--jenkins-proxy-url", action="store", help="", default="https://idler.openshift.io")

@pytest.fixture
def openshift_api_token():
    # use get instead of [ ] so that we can print a better error message
    # instead of KeyError
    token = os.environ.get('OPENSHIFT_API_TOKEN', None)
    assert token, 'OPENSHIFT_API_TOKEN environment variable must be set'
    return token


@pytest.fixture
def jenkins_proxy_url(request):
    return request.config.getoption("--jenkins-url")

@pytest.fixture
def idler_url(request):
    return request.config.getoption("--idler-url")

class Idler:
    def __init__(self, req):
        self.req = req

    def idle_jenkins(self):
        print(" .. idling jenkins")
        self.req

class Jenkins:
    def __init__(self, req):
        self.req = req

    @property
    def status(self):
        print("Getting status")
        return "offline"

@pytest.fixture
def idler(openshift_api_token):
    return Idler('req')


@pytest.fixture
def jenkins(openshift_api_token):
    return Jenkins('req')
