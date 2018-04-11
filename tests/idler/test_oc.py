#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_get_projects(oc):
    projects = oc.projects
    assert projects, "get projects returned empty"


def test_jenkins_project(oc):
    jenkins = oc.jenkins_project
    assert jenkins, "Jenkins Project could not be found"
