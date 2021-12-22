import logging
import os
from threading import Thread

import defaults
from app.common.zeebe_consumer_service.zeebe_consumer_service import ZeebeConsumerService

zeebe_server = os.getenv("ZEEBE_URL")
task_type = "notify_client"


def process_order_action(job):
    logging.info("job processed: {job}")


num_threads = int(os.getenv("THREADS_COUNT"))
for _ in range(num_threads):
    Thread(group=None, target=ZeebeConsumerService(zeebe_server,
                                                   task_type,
                                                   process_order_action).start).start()


