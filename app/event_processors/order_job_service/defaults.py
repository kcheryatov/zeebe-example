import os
import logging

os.environ.setdefault('LOGS_FILE', 'logs/order_job_consumer_service_local.log')
os.environ.setdefault('THREADS_COUNT', '1')

os.environ.setdefault('ZEEBE_URL', '192.1.1.5:26500')

logging.basicConfig(
    filename=os.getenv('LOGS_FILE'),
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
