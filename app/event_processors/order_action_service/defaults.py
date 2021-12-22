import os
import logging

os.environ.setdefault('LOGS_FILE', 'logs/order_action_kafka_event_consumer_service_local.log')
os.environ.setdefault('KAFKA_URL', '192.1.1.5:9093')
os.environ.setdefault('ORDER_ACTION_TOPICS_MAPPINGS', '{"validation":"order_validated",'
                                                      '"activation":"order_activated,'
                                                      '"completion":"order_completed",'
                                                      '"ext_validation":"order_ext_validated",'
                                                      '"calcellation":"order_cancelled"}')
os.environ.setdefault('THREADS_COUNT', '4')

os.environ.setdefault('ZEEBE_URL', '192.1.1.5:26500')

logging.basicConfig(
    filename=os.getenv('LOGS_FILE'),
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
