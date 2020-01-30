from cashier_service.infrastructure.event_publisher import EventPublisher
from cashier_service.mock.mock_config import MockConfig
from unittest.mock import patch, Mock
from concurrent.futures import Future
from json import dumps
import os

test_credentials_path = "./tests/cashier_service/mock/dummy_cred.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = test_credentials_path


def test_event_publisher_sets_topic_correctly():
    config = MockConfig("test_topic", "test_project")
    publisher = EventPublisher(config)

    assert publisher.topic == 'projects/test_project/topics/test_topic'


@patch("google.cloud.pubsub.PublisherClient.publish")
def test_event_publisher_sends_message_info_correctly(publish):
    mock_future = Mock(Future())
    publish.return_value = mock_future
    config = MockConfig("test_topic", "test_project")
    publisher = EventPublisher(config)
    event = dumps(dict(accountNumber="12345678", clearedBalance=500))

    publisher.produce(event)

    publish.assert_called_with("projects/test_project/topics/test_topic",
                               bytes(event, 'utf-8'))
    mock_future.result.assert_called_once()
