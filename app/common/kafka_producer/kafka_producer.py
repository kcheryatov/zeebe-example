from confluent_kafka import Producer
import socket
import logging


class KafkaProducer:
    def __init__(self, kafka_servers):
        self.__producer__ = Producer({'bootstrap.servers': kafka_servers,
                                      'client.id': socket.gethostname()})

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            logging.error('Message delivery failed: {} {} {}'.format(msg.topic(), msg.partition(), err))
        else:
            logging.debug('Message delivery ok: {} {} {}'.format(msg.topic(), msg.partition(), err))

    def send_message(self, topic_name, body):
        try:
            self.__producer__.produce(topic_name, body,
                                      callback=KafkaProducer.delivery_report)
            self.__producer__.flush()
            logging.debug("Message flushed")
        except Exception as ex:
            logging.error("Error while send message: {}".format(ex))
            raise
