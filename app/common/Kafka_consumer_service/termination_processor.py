import signal
import atexit
import logging


class TerminationProcessor:
    def __init__(self, stop_func):
        signal.signal(signal.SIGINT, self.__exit_gracefully__)
        signal.signal(signal.SIGTERM, self.__exit_gracefully__)

        logging.info("TerminationProcessor: SIGTERM subscribed")

        self.stop_func = stop_func
        atexit.register(self.stop_func)

    def __exit_gracefully__(self, *args):
        self.stop_func()
        logging.info("TerminationProcessor: __exit_gracefully__ called")
