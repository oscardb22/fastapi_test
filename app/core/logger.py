import contextvars
import logging
import sys

import uvicorn.logging

requester_id = contextvars.ContextVar("requester_id", default="system")
FORMAT: str = "%(levelprefix)s [%(requester_id)s] [%(asctime)s] [%(name)s] %(message)s (%(filename)s:%(lineno)d)"


def _setup_record_factory():
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.requester_id = requester_id.get()
        return record

    logging.setLogRecordFactory(record_factory)
    logging.getLogRecordFactory().requester_id_added = True


def setup_logger(name, log_file="logfile.log", level=logging.DEBUG):
    current_factory = logging.getLogRecordFactory()
    if not hasattr(current_factory, "requester_id_added"):
        _setup_record_factory()

    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Create formatters and add them to the handlers
    formatter = uvicorn.logging.DefaultFormatter(FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger if not already added
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.info("Hello, world!")
