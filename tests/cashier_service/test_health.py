from unittest.mock import Mock

import pytest

from cashier_service.app import create
from cashier_service.mock.mock_events import MockEvents
from cashier_service.settings import config


@pytest.fixture(scope='function')
def web_client():
    broker = MockEvents()
    return create(config=config['development'],
                  broker=broker).test_client()

def test_should_have_web_client(web_client):
    response = web_client.get('/cashier/health')
    assert response.status_code == 200, f'Expected status code to be 200; got {response.status_code}'  # noqa
    assert response.is_json, f'Expected content type to be JSON; got "{response.data}'  # noqa
    assert response.get_json() == {'message': 'OK'}, f'Unexpected JSON; got {repr(response.get_json())}'  # noqa
