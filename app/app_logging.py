"""Logging module for the planning app."""
import logging
from datetime import datetime
from pathlib import Path


def setup_logging():
    """Setup logging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # create logs folder if it doesn't exist
    Path("logs").mkdir(parents=True, exist_ok=True)

    # Initialize logging
    logging.basicConfig(
        filename=f"logs/io_log_{timestamp}.txt",
        level=logging.INFO,
        format="%(message)s",
    )
