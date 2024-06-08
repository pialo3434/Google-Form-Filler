# handler.py
import os
import logging
import time

# Get the absolute path of the directory of this file
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create the logs directory if it does not exist
logs_dir = os.path.join(dir_path, 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

def setup_logger():
    # Create a logger
    logger = logging.getLogger('form_logger')
    logger.setLevel(logging.INFO)

    # Create a file handler
    log_file = os.path.join(logs_dir, f'log_{time.strftime("%Y%m%d-%H%M%S")}.txt')
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - Question: %(message)s')
    handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(handler)

    return logger
