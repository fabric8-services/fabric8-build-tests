#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `fabric8_build_tests` package."""

def test_idle(idler, jenkins):
    """ Idler can put jenkins to sleep """
    idler.idle_jenkins
    assert jenkins.status == 'offline'


#  def test_jenkins_wakes_up_on_webhook(idler, jenkins):
    #  assert jenkins.status == 'offline'
    #  jenkins.send_webhook
    #  assert jenkins.status == 'online'
