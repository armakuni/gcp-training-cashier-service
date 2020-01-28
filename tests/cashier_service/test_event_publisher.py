from cashier_service.infrastructure.event_publisher import EventPublisher
from cashier_service.mock.mock_config import MockConfig
from unittest.mock import patch, Mock
from concurrent.futures import Future
from json import dumps


@patch("google.cloud")
def test_event_publisher_sets_topic_correctly(cloud):
    cloud.pubsub.PublisherClient.return_value = Mock()
    config = MockConfig("test_topic", "test_project")
    publisher = EventPublisher(config, cloud.pubsub)

    assert publisher.topic == 'projects/test_project/topics/test_topic'


@patch("google.cloud")
def test_event_publisher_sends_message_info_correctly(cloud):
    mock_future = Mock(Future())
    cloud.pubsub.PublisherClient.return_value.publish.return_value = mock_future
    config = MockConfig("test_topic", "test_project")
    publisher = EventPublisher(config, cloud.pubsub)
    event = dumps(dict(accountNumber="12345678", clearedBalance=500))

    publisher.produce(event)

    cloud.pubsub.PublisherClient.return_value.publish.assert_called_with("projects/test_project/topics/test_topic",
                               bytes(event, 'utf-8'))
    mock_future.result.assert_called_once()
