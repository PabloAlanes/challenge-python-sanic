import pika
from settings.rabbitmq import *
import time

def callback(ch, method, properties, body):
    print(f'Received transaction ID:{body.decode()}')
    time.sleep(10)
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
