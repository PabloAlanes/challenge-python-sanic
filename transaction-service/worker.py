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
    except requests.exceptions.ConnectionError:
        logger.error('Error to get transaction data')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.error(f'Finish transaction ID:{body.decode()}')
        return


    try:
        if ACCOUNT_SVC_ENABLED:
            # Load accounts data
            acc_source_resp = requests.get(f'{ACCOUNT_SVC_URL}/accounts/{transaction.get("source")}')
            acc_dest_resp = requests.get(f'{ACCOUNT_SVC_URL}/accounts/{transaction.get("destiny")}')

            # Update accounts data
            new_acc_dest = acc_dest_resp.json().get('money') + transaction.get("amount")
            new_acc_source = acc_source_resp.json().get('money') - transaction.get("amount")

            requests.put(f'{ACCOUNT_SVC_URL}/accounts/{transaction.get("source")}',
                         json={"money": new_acc_source}, headers=headers)
            requests.put(f'{ACCOUNT_SVC_URL}/accounts/{transaction.get("destiny")}',
                         json={"money": new_acc_dest}, headers=headers)

        # Update transaction status
        requests.put(f'{TRANSACTION_SVC_URL}/transactions/{transaction_id}',
                     json={"status": "done"}, headers=headers)

    except requests.exceptions.ConnectionError:
        logger.error('Error to update accounts')
        requests.put(f'{TRANSACTION_SVC_URL}/transactions/{transaction_id}',
                     json={"status": "error"}, headers=headers)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.info(f'Finish transaction ID:{transaction_id}')


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
