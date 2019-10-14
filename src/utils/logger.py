import logging


class Logger:
    def __init__(self, logging_level=logging.INFO):
        logging.basicConfig(level=logging_level)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

        std_handler, file_handler = self._create_handlers()
        std_format, file_format = self._create_formatters()

        std_handler.setFormatter(std_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        self.logger.addHandler(std_handler)
        self.logger.addHandler(file_handler)

    @staticmethod
    def _create_handlers(std_logging_level=logging.WARNING,
                         file_logging_level=logging.ERROR):
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('file.log')
        c_handler.setLevel(std_logging_level)
        f_handler.setLevel(file_logging_level)

        return c_handler, f_handler

    @staticmethod
    def _create_formatters():
        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        return c_format, f_format

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg=msg)

    def info(self, msg):
        self.logger.info(msg)


def get_logger():
    return Logger()
