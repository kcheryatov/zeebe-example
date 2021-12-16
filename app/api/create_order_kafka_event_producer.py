import os
import logging
import json

import defaults
from app.common.kafka_producer.kafka_producer import KafkaProducer


class CreateOrderKafkaProducer:
    def __get_env_vars__(self):
        self.__kafka_servers__ = os.getenv("KAFKA_URL")
        self.__topic_name__ = os.getenv("KAFKA_ORDER_NEW_TOPIC")

    def __init__(self):
        try:
            self.__get_env_vars__()
            self.__producer__ = KafkaProducer(self.__kafka_servers__)
        except Exception as ex:
            logging.error("Error while create kafka producer {}".format(ex))
            raise

    def send_message(self, order):
        try:
            str_order = json.dumps(order).encode('utf-8')
            self.__producer__.send_message(self.__topic_name__, str_order)
            logging.debug("Topic {} Message ready: {}".format(self.__topic_name__, str_order))
        except Exception as ex:
            logging.error("Error while create send message to kafka {}".format(ex))
            raise

