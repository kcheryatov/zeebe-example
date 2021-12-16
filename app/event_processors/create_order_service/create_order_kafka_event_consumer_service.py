import logging
import os
from threading import Thread

import defaults
from app.common.Kafka_consumer_service.kafka_consumer_service import KafkaConsumerService

kafka_servers = os.getenv("KAFKA_URL")
topic_name = os.getenv("KAFKA_ORDER_NEW_TOPIC")

num_threads = int(os.getenv("THREADS_COUNT"))

for _ in range(num_threads):
    Thread(group=None, target=KafkaConsumerService(kafka_servers,
                                                   "KafkaConsumerService",
                                                   topic_name,
                                                   logging.info).start).start()


