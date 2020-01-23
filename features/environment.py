from cashier_service import app
from cashier_service.mock.mock_events import MockEvents
from cashier_service.settings import config


def before_all(context):
    context.broker = MockEvents()
    context.web_client = app.create(config=config['testing'],
                                    broker=context.broker).test_client()
