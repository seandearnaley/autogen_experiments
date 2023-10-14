"""Logging module for the planning app."""
import logging
from datetime import datetime


def setup_logging():
    """Setup logging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Initialize logging
    logging.basicConfig(
        filename=f"logs/io_log_{timestamp}.txt",
        level=logging.INFO,
        format="%(message)s",
    )
