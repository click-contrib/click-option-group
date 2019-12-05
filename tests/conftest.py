# -*- coding: utf-8 -*-

from click.testing import CliRunner

import pytest


@pytest.fixture(scope='function')
def runner():
    return CliRunner()
