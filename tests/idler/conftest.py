import pytest
import os
import json
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
        self._project = ''

    def run(self, command, json=True):
        oc_parts = ['oc']

        if self._project:
            oc_parts += ['-n=' + self._project]

        subcmd_parts = command.split(' ')
        if json:
            subcmd_parts += ['-o=json']

        # safe cmd must not have any secrets
        safe_cmd = ' '.join([*oc_parts, *subcmd_parts])

        secrets = [
            '--server=' + self.openshift_url,
            '--token=' + self.openshift_token,
        ]

        cmd = [*oc_parts, *secrets, *subcmd_parts]

        print("Running: ", safe_cmd)
        # TODO(sthaha):delme
        #  __import__('ipdb').set_trace()
        proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if proc.returncode != 0:
            raise RuntimeError("Failed to execute: " + safe_cmd)

        return str(proc.stdout, 'utf-8')

    @property
    def project_names(self):
        ret = self.run('get projects')
        return jq('.items[].metadata.name').transform(
            text=ret, multiple_output=True)

    @property
    def project(self):
        """returns current project name"""
        if not self._project:
            self._project = self.run('project -q', json=False).strip()
        return self._project

    @project.setter
    def project(self, v):
        self._project = v

    @property
    def pods(self):
        """Returns a dict/json representation of pods running in current project """
        return json.loads(self.run('get pods'))


@pytest.fixture
def oc(openshift_url, openshift_token):
    client = OpenshiftClient(openshift_url, openshift_token)
    return client

@pytest.fixture
def jenkins(oc):
    return Jenkins(oc)
