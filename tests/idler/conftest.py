import pytest
import os
from jq import jq
import subprocess

def pytest_addoption(parser):
    parser.addoption("--osio-url", action="store",
                     help="",
                     default="https://openshift.io")
    parser.addoption("--osio-api-url", action="store",
                     help="", default="https://api.openshift.io")
    parser.addoption("--jenkins-proxy-url", action="store",
                     help="",
                     default="https://jenkins.openshift.io")
    parser.addoption("--openshift-url", action="store",
                     help="",
                     default="https://console.starter-us-east-2.openshift.com")

@pytest.fixture
def openshift_url(request):
    return request.config.getoption("--openshift-url")

@pytest.fixture
def openshift_token():
    # use get instead of [ ] so that we can print a better error message
    # instead of KeyError
    token = os.environ.get('OPENSHIFT_TOKEN', None)
    assert token, 'OPENSHIFT_TOKEN environment variable must be set'
    return token


@pytest.fixture
def jenkins_proxy_url(request):
    return request.config.getoption("--jenkins-url")


class Jenkins:
    def __init__(self, req, oc):
        self.req = req
        self.oc = oc

    @property
    def status(self):
        # oc
        print("Getting status")
        self.oc.run('get pods')
        return "offline"


class OpenshiftClient:
    def __init__(self, openshift_url, openshift_token):
        self.openshift_url = openshift_url
        self.openshift_token = openshift_token
        self._jenkins_project = ''

    def run(self, sub_command, json=True):
        #  self.login()

        output_format = '-o=json' if json else ''
        cmd = [
            'oc',
            '--server=' + self.openshift_url,
            '--token=' + self.openshift_token,
            *sub_command.split(' '),
            output_format
        ]

        print("Running command: oc " + sub_command)
        proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if proc.returncode != 0:
            raise "Failed to execute oc " + sub_command

        return str(proc.stdout, 'utf-8')

    @property
    def projects(self):
        ret = self.run('get projects')
        return jq('.items[].metadata.name').transform(text=ret, multiple_output=True)

    @property
    def jenkins_project(self):
        if self._jenkins_project:
            return self._jenkins_project

        ret = self.run('get projects')
        query = '.items[].metadata.name|select(endswith("-jenkins"))'
        self._jenkins_project = jq(query).transform(text=ret)
        return self._jenkins_project


@pytest.fixture
def oc(openshift_url, openshift_token):
    client = OpenshiftClient(openshift_url, openshift_token)
    return client


@pytest.fixture
def jenkins(oc):
    return Jenkins('req', oc)
