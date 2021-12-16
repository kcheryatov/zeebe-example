import os
import logging

os.environ.setdefault('LOGS_FILE', 'create_order_service/logs/create_order_kafka_event_consumer_service_local.log')
os.environ.setdefault('KAFKA_URL', 'localhost:9093')
os.environ.setdefault('KAFKA_ORDER_NEW_TOPIC', 'order_new_topic')
os.environ.setdefault('THREADS_COUNT', '4')


logging.basicConfig(
    filename=os.getenv('LOGS_FILE'),
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
