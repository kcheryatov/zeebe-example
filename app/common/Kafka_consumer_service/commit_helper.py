import time

class CommitHelper:
    def __init__(self, seconds_between_commits, messages_between_commits):
        self.__seconds_between_commits__ = seconds_between_commits
        self.__messages_between_commits__ = messages_between_commits

        self.__messages_counter__ = 0
        self.__time__ = time.time()

    def clear(self):
        self.__messages_counter__ = 0
        self.__time__ = time.time()

    def inc_message(self):
        self.__messages_counter__ += 1

    def need_commit(self):
        return self.__messages_counter__ == 50 or self.__messages_counter__ > self.__messages_between_commits__ and \
               time.time() - self.__time__ >= self.__seconds_between_commits__
