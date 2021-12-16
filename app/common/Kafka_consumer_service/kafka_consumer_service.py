import logging
import time

from confluent_kafka import Consumer

from app.common.Kafka_consumer_service.commit_helper import CommitHelper
from app.common.Kafka_consumer_service.termination_processor import TerminationProcessor


SECONDS_BETWEEN_POOLS = 0.05
SECONDS_BETWEEN_COMMITS = 5
MESSAGES_BETWEEN_COMMITS = 50


class KafkaConsumerService:

    def __init_consumer__(self, kafka_servers, group_id, topic_name):
        self.__consumer__ = Consumer({
            'bootstrap.servers': kafka_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'metadata.max.age.ms': '1000'
        })

        self.__consumer__.subscribe([topic_name])
        logging.info("subscribed to topic '{}'".format(topic_name))

    def __init_terminator__(self):
        self.__stop_flag__ = False

        def set_stop_flag_true_func(): self.__stop_flag__ = True
        self.___terminator__ = TerminationProcessor(set_stop_flag_true_func)

    def __init__(self, kafka_servers, group_id, topic_name, process_message_func):
        self.__init_consumer__(kafka_servers, group_id, topic_name)
        self.__init_terminator__()
        self.__commit_helper__ = CommitHelper(SECONDS_BETWEEN_COMMITS, MESSAGES_BETWEEN_COMMITS)

        self.__process_message_func__ = process_message_func

    def __receive_and_process_message__(self):
        try:
            msg = self.__consumer__.poll(timeout=0.1)

            if msg is not None:
                self.__process_message_func__(msg.value())
                self.__commit_helper__.inc_message()
                if msg.error():
                    logging.error("Consumer error: {}".format(msg.error()))
            else:
                logging.debug("No message received")
        except Exception as ex:
            logging.error("Error while receive message: {}".format(ex))

    def start(self):
        try:
            self.__commit_helper__.clear()
            while not self.__stop_flag__:
                self.__receive_and_process_message__()

                if self.__commit_helper__.need_commit():
                    self.__consumer__.commit(asynchronous=True)
                    self.__commit_helper__.clear()
                    logging.debug("messages committed")
                time.sleep(SECONDS_BETWEEN_POOLS)
        finally:
            self.stop()

    def stop(self):
        if self.__commit_helper__.need_commit():
            self.__consumer__.commit(asynchronous=False)
        self.__consumer__.close()
        logging.info("Finally messages committed and consumer closed")
