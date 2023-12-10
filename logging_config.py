import logging
import os
from datetime import datetime

def setup_logging():
    """Set up logging with a file handler."""
    log_filename = get_current_log_filename()
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename=log_filename, level=logging.DEBUG)

def get_current_log_filename():
    """Generates a filename for the current log file based on the date and time."""
    # Including hours, minutes, and seconds in the filename
    return datetime.now().strftime("logs/cmdgptlog%Y%m%d%H%M%S.txt")

