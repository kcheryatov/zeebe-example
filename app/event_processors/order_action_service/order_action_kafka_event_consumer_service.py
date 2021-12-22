import logging
import os
import json
from threading import Thread

import defaults
from app.common.Kafka_consumer_service.kafka_consumer_service import KafkaConsumerService
from app.common.kafka_producer.kafka_producer import KafkaProducer

from app.common.Kafka_consumer_service.termination_processor import TerminationProcessor


kafka_servers = os.getenv("KAFKA_URL")
topic_name = "order_before_action_events"


def get_action_type_map():
    setting = os.getenv("ORDER_ACTION_TOPICS_MAPPINGS")
    logging.info("Action type mapping loaded: {}".format(setting))
    return json.loads(setting)


action_type_map = get_action_type_map()


class ProcessOrderAction:

    def __init__(self, order_before_action_events_topic_name):
        try:
            self.__kafka_servers__ = kafka_servers
            self.__topic_name__ = order_before_action_events_topic_name
            self.__producer__ = KafkaProducer(self.__kafka_servers__)
        except Exception as ex:
            logging.error("Error while create kafka producer {}".format(ex))
            raise

    def send_message(self, message):
        try:
            str_message = json.dumps(message).encode('utf-8')
            self.__producer__.send_message(self.__topic_name__, str_message)
            logging.info("Topic {} Message ready: {}".format(self.__topic_name__, message))
        except Exception as ex:
            logging.error("Error while create send message to kafka {}".format(ex))
            raise

def get_result(order_id):
    if int(order_id) % 5 == 0:
        return "notOk"
    else:
        return "Ok"

def process_order_action(order_action_message):
    order_action = json.loads(json.loads(order_action_message))
    print(order_action)

    action_type = order_action["variablesAsMap"]["actionType"]
    order_id = order_action["variablesAsMap"]["orderId"]
    res_topic_name = action_type_map[action_type]

    res_message = {"orderId": order_id, "messageName": res_topic_name, "result": get_result(order_id)}
    ProcessOrderAction(res_topic_name).send_message(res_message)


num_threads = int(os.getenv("THREADS_COUNT"))
for _ in range(num_threads):
    Thread(group=None, target=KafkaConsumerService(kafka_servers,
                                                   "OrderActionsConsumerService_13",
                                                   topic_name,
                                                   process_order_action).start).start()


