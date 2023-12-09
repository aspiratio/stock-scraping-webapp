import logging


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)


if __name__ == "__main__":
    logger = Logger(__name__)
    logger.info("Hello, world!")
