"""
Handle HTTP requests with retry logic and error handling
"""

import requests
from logger import get_logger
from config import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT, DEFAULT_RETRIES
import time

logger = get_logger()

class RequestHandler:
    def __init__(self):
        """Initialize request handler"""
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': DEFAULT_USER_AGENT})
        logger.info("RequestHandler initialized")
    
    def get(self, url, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES):
        """
        Make GET request with retry logic
        
        Args:
            url: URL to request
            timeout: Request timeout in seconds
            retries: Number of retry attempts
            
        Returns:
            Response object or None on failure
        """
        for attempt in range(retries):
            try:
                logger.debug(f"GET request to {url} (attempt {attempt + 1}/{retries})")
                
                response = self.session.get(
                    url,
                    timeout=timeout,
                    allow_redirects=True
                )
                
                response.raise_for_status()
                logger.info(f"✓ Request successful: {url}")
                return response
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP Error: {e.response.status_code}")
                return None
                
            except Exception as e:
                logger.error(f"Error during request: {str(e)}")
                return None
        
        logger.error(f"Failed after {retries} attempts: {url}")
        return None
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.info("RequestHandler session closed")
