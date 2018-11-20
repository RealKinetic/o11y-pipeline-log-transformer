import base64
import json
import logging
import os

from google.cloud import pubsub_v1


publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv('GCP_PROJECT'),
                                  os.getenv('TOPIC_NAME'))


def handle_log(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    if 'data' not in event:
        logging.warn("No 'data' field in pub/sub message")
        return

    data = base64.b64decode(event['data']).decode('utf-8')
    return publish_data(transform_log(data))


def transform_log(data):
    return json.dumps({
        'type': 'LOG',
        'version': 1,
        'payload': data,
    }).encode('utf-8')


def publish_data(data):
    future = publisher.publish(topic_path, data=data)
    future.add_done_callback(callback)


def callback(future):
    if future.exception(timeout=30):
        raise future.exception()
    else:
        logging.info('Wrote transformed data to {}'.format(topic_path))
