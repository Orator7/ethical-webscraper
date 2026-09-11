"""
Logging setup for the web scraper
"""

import logging
import os
from config import LOG_LEVEL, LOG_FILE

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("webscraper")
logger.setLevel(getattr(logging, LOG_LEVEL))

# File handler
file_handler = logging.FileHandler(f"logs/{LOG_FILE}")
file_handler.setLevel(getattr(logging, LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, LOG_LEVEL))

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
