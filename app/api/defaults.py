import os
import logging

os.environ.setdefault('LOGS_FILE', './logs/create_order_api_local.log')
os.environ.setdefault('KAFKA_URL', 'localhost:9093')
os.environ.setdefault('KAFKA_ORDER_NEW_TOPIC', 'order_new_topic')

logging.basicConfig(
    filename=os.getenv('LOGS_FILE'),
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
