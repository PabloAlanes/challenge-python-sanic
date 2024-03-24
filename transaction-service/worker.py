import pika
import requests
from settings.rabbitmq import *
from settings.services import *
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)


def callback(ch, method, properties, body):
    logger.info(f'Received transaction ID:{body.decode()}')
    transaction_id = body.decode()

    headers = {'Content-Type': 'application/json'}

    try:
        # Load transaction data
        transaction_resp = requests.get(f'{TRANSACTION_SVC_URL}/transactions/{transaction_id}',
                                        headers=headers)
        transaction = transaction_resp.json()
        logger.info(transaction)

        # Update transaction status
        requests.put(f'{TRANSACTION_SVC_URL}/transactions/{transaction_id}',
                     json={"status": "done"}, headers=headers)

    except requests.exceptions.ConnectionError:
        logger.error('Error to get transaction data')

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info(f'Finish transaction ID:{body.decode()}')


if __name__ == '__main__':
    logger.info('Run WORKER to do the transactions. To exit press CTRL+C')
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()
