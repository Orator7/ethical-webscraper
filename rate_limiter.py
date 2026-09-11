"""
Rate limiting to ensure we don't overload servers
"""

import time
from datetime import datetime, timedelta
from collections import defaultdict
from logger import get_logger
from config import DEFAULT_DELAY_BETWEEN_REQUESTS, DEFAULT_REQUESTS_PER_MINUTE

logger = get_logger()

class RateLimiter:
    def __init__(self, delay=DEFAULT_DELAY_BETWEEN_REQUESTS, requests_per_minute=DEFAULT_REQUESTS_PER_MINUTE):
        """
        Initialize rate limiter
        
        Args:
            delay: Minimum delay between requests in seconds
            requests_per_minute: Maximum requests allowed per minute
        """
        self.delay = delay
        self.requests_per_minute = requests_per_minute
        self.last_request_time = {}
        self.request_history = defaultdict(list)
    
    def wait(self, domain):
        """
        Wait if necessary to respect rate limits
        
        Args:
            domain: The domain being scraped (e.g., 'example.com')
        """
        current_time = time.time()
        
        # Check delay between requests
        if domain in self.last_request_time:
            elapsed = current_time - self.last_request_time[domain]
            if elapsed < self.delay:
                wait_time = self.delay - elapsed
                logger.info(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
                time.sleep(wait_time)
        
        # Check requests per minute
        self._cleanup_old_requests(domain)
        
        if len(self.request_history[domain]) >= self.requests_per_minute:
            oldest_request = self.request_history[domain][0]
            time_since_oldest = current_time - oldest_request
            
            if time_since_oldest < 60:
                wait_time = 60 - time_since_oldest
                logger.warning(f"Rate limit reached for {domain}: waiting {wait_time:.2f}s")
                time.sleep(wait_time)
                self._cleanup_old_requests(domain)
        
        # Record this request
        self.request_history[domain].append(current_time)
        self.last_request_time[domain] = current_time
        logger.debug(f"Request made to {domain}")
    
    def _cleanup_old_requests(self, domain):
        """Remove requests older than 1 minute"""
        current_time = time.time()
        self.request_history[domain] = [
            req_time for req_time in self.request_history[domain]
            if current_time - req_time < 60
        ]
    
    def set_limits(self, domain, delay, requests_per_minute):
        """Update rate limits for a specific domain"""
        self.delay = delay
        self.requests_per_minute = requests_per_minute
        logger.info(f"Updated rate limits for {domain}: {delay}s delay, {requests_per_minute} req/min")
