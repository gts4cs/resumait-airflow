from __future__ import annotations

import logging


def setup_logger(log_file="crawler.log"):
    """
    Configures and returns a logger for logging messages to a specified file.

    Parameters:
        log_file (str): The name of the log file. Default is "crawler.log".

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()
