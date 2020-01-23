from google.cloud import pubsub
import logging


class EventPublisher:

    def __init__(self, config):
        self.client = pubsub.PublisherClient()
        topic_name = config.TOPIC_NAME
        project = config.PROJECT_ID
        self.topic = f"projects/{project}/topics/{topic_name}"

    def produce(self, event):
        future = self.client.publish(self.topic, bytes(event, 'utf-8'))
        message_id = future.result()
        logging.info("Message ID: " + message_id)
