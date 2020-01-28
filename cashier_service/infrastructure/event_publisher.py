import logging


class EventPublisher:

    def __init__(self, config,pubsub):
        self.client = pubsub.PublisherClient()
        self.topic = f"projects/{config.PROJECT_ID}/topics/{config.TOPIC_NAME}"

    def produce(self, event):
        future = self.client.publish(self.topic, bytes(event, 'utf-8'))
        message_id = future.result()
        logging.info("Message ID: " + str(message_id))
