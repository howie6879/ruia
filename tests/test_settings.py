#!/usr/bin/env python

import os

import pytest

from ruia.wrappers import SettingsWrapper

s = SettingsWrapper()


def test_settings_load_with_file():
    s.load_with_file('./tests/settings.py')
    assert s.my_settings.get('REQUEST_CONFIG', None)['DELAY'] == 5


def test_settings_load_with_dict():
    request_config = {
        'DELAY': 10,
    }
    s.load_with_dict(request_config)
    assert s.my_settings.get('DELAY', None) == 10


def test_settings_load_with_env():
    os.environ = {
        'RUIA_DELAY':15,
    }
    s.load_from_environment()
    assert s.my_settings.get('DELAY', None) == 15
