"""
Configuration settings for the ethical web scraper
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Request settings
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
DEFAULT_TIMEOUT = 10  # seconds
DEFAULT_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5  # exponential backoff

# Rate limiting (be polite to servers)
DEFAULT_DELAY_BETWEEN_REQUESTS = 2  # seconds
DEFAULT_REQUESTS_PER_MINUTE = 20  # respectful limit

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "scraper.log"

# Cache settings
CACHE_ENABLED = True
CACHE_DURATION = 3600  # 1 hour in seconds
CACHE_DIR = ".cache"

# Browser settings for JavaScript-heavy sites
HEADLESS_BROWSER = True
BROWSER_TIMEOUT = 30  # seconds

# Proxy settings (optional)
USE_PROXY = os.getenv("USE_PROXY", "False").lower() == "true"
PROXY_LIST = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []

# Site-specific configs (customize as needed)
SITE_CONFIGS = {
    "default": {
        "delay": DEFAULT_DELAY_BETWEEN_REQUESTS,
        "requests_per_minute": DEFAULT_REQUESTS_PER_MINUTE,
        "timeout": DEFAULT_TIMEOUT,
    },
    "example.com": {
        "delay": 3,  # More delay for stricter sites
        "requests_per_minute": 10,
        "timeout": 15,
        "requires_js": False,
    }
}
