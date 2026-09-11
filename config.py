"""
Configuration settings for the web scraper
"""

# Request settings
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 3
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Rate limiting
DEFAULT_DELAY_BETWEEN_REQUESTS = 2  # seconds
DEFAULT_REQUESTS_PER_MINUTE = 20

# Caching
CACHE_ENABLED = True
CACHE_DURATION = 3600  # 1 hour

# Site-specific configurations
SITE_CONFIGS = {
    "default": {
        "delay": 2,
        "requests_per_minute": 20,
        "timeout": 10
    },
    "www.bbc.com": {
        "delay": 3,
        "requests_per_minute": 10,
        "timeout": 15
    },
    "github.com": {
        "delay": 2,
        "requests_per_minute": 30,
        "timeout": 10
    }
}
