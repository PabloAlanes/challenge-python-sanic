import pika
import requests
from settings.rabbitmq import *
from settings.services import *

def callback(ch, method, properties, body):
    print(f'Received transaction ID:{body.decode()}')
    transaction_id = body.decode()

    headers = {'Content-Type': 'application/json'}

    try:
        # Load transaction data
        transaction_resp = requests.get(f'{TRANSACTION_SVC_URL}/transactions/{transaction_id}',
                                        headers=headers)
        transaction = transaction_resp.json()
        print(transaction)

        # Update transaction status
        requests.put(f'{TRANSACTION_SVC_URL}/transactions/{transaction_id}',
                     json={"status": "done"}, headers=headers)

    except requests.exceptions.ConnectionError:
        print('Error to get transaction data')

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f'Finish transaction ID:{body.decode()}')


if __name__ == '__main__':
    print('Run WORKER to do the transactions. To exit press CTRL+C')
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
