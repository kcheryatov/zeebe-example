import logging
import time
import grpc
import json
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc

from app.common.zeebe_consumer_service.termination_processor import TerminationProcessor


class ZeebeConsumerService:

    def __init_consumer__(self, zeebe_server):

        self.__channel__ = grpc.insecure_channel(zeebe_server)
        self.__stub__ = gateway_pb2_grpc.GatewayStub(self.__channel__)

        logging.info("task type consumer created '{}'".format(zeebe_server))

    def __init_terminator__(self):
        self.__stop_flag__ = False

        def set_stop_flag_true_func(): self.__stop_flag__ = True
        self.___terminator__ = TerminationProcessor(set_stop_flag_true_func)

    def __init__(self, zeebe_server, task_type, process_message_func):
        self.__init_consumer__(zeebe_server)
        self.__init_terminator__()

        self.__process_message_func__ = process_message_func

        self.__task_type__ = task_type

    def __receive_and_process_message__(self):
        try:
            activate_jobs_response = self.__stub__.ActivateJobs(
                gateway_pb2.ActivateJobsRequest(
                    type=self.__task_type__,
                    worker="worker",
                    timeout=60000,
                    maxJobsToActivate=1))

            if activate_jobs_response is not None:
                for activate_job_response in activate_jobs_response:
                    for job in activate_job_response.jobs:
                        try:
                            self.__process_message_func__(job)
                            self.__stub__.CompleteJob(gateway_pb2.CompleteJobRequest(jobKey=job.key, variables="{}"))
                        except Exception as e:
                            logging.error("Error while job '{job}' processing: {e}")
                            self.__stub__.FailJob(gateway_pb2.FailJobRequest(jobKey=job.key))
            else:
                logging.debug("No message received")
        except Exception as ex:
            logging.error("Error while receive message: {}".format(ex))

    def start(self):
        try:
            while not self.__stop_flag__:
                self.__receive_and_process_message__()
                logging.debug("messages committed")
        finally:
            self.stop()

    def stop(self):
        self.__channel__.close()
        logging.info("Finally channel closed")
