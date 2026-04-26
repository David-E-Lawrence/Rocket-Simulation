import logging
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
import os
import queue

def get_logger(config, run_dir):
    logger = logging.getLogger("Rocket_Simulation")
    logger.setLevel(logging.DEBUG)

    # Avoid adding multiple handlers if the logger already has them
    if logger.handlers:
        return logger
    
    # making log directory
    log_dir=os.path.join(run_dir, "log")
    os.makedirs(log_dir)

    # Debug file handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "Rocket_Simulation.log"),
        maxBytes=1024*1024*config["max_log_file_size"],
        backupCount=1000
        )

    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    ))

    file_handler.setLevel(config["log_level"]["file"])

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        "%(name)s | %(message)s"
    ))

    stream_handler.setLevel(config["log_level"]["console"])

    logger.addHandler(stream_handler)

    # adding log queue handler

    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    listener = QueueListener(log_queue, file_handler, respect_handler_level=True)
    listener.start()

    return logger, listener