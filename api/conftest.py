import pytest
import os
import application
import sys

sys.dont_write_bytecode = True


@pytest.yield_fixture(scope="session")
def app():
    os.environ['POSTGRES_DB'] = 'test'
    yield application.create('test_api')
