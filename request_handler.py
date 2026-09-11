"""
Handle HTTP requests with retry logic and error handling
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from logger import get_logger
from config import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT, DEFAULT_RETRIES, DEFAULT_BACKOFF_FACTOR

logger = get_logger()

class RequestHandler:
    def __init__(self, user_agent=DEFAULT_USER_AGENT, timeout=DEFAULT_TIMEOUT, retries=DEFAULT_RETRIES):
        """
        Initialize request handler
        
        Args:
            user_agent: User agent string for requests
            timeout: Request timeout in seconds
            retries: Number of retries on failure
        """
        self.user_agent = user_agent
        self.timeout = timeout
        self.retries = retries
        self.session = self._create_session()
    
    def _create_session(self):
        """Create a requests session with retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.retries,
            backoff_factor=DEFAULT_BACKOFF_FACTOR,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def get(self, url, headers=None, **kwargs):
        """
        Make a GET request
        
        Args:
            url: URL to request
            headers: Optional custom headers
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            requests.Response: Response object or None on failure
        """
        default_headers = {
            'User-Agent': self.user_agent,
        }
        
        if headers:
            default_headers.update(headers)
        
        try:
            logger.info(f"Making GET request to {url}")
            response = self.session.get(
                url,
                headers=default_headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            logger.debug(f"Response status: {response.status_code}")
            return response
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while requesting {url}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while requesting {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error requesting {url}: {str(e)}")
            return None
    
    def post(self, url, data=None, json=None, headers=None, **kwargs):
        """
        Make a POST request
        
        Args:
            url: URL to request
            data: Form data
            json: JSON data
            headers: Optional custom headers
            **kwargs: Additional arguments
            
        Returns:
            requests.Response: Response object or None on failure
        """
        default_headers = {
            'User-Agent': self.user_agent,
        }
        
        if headers:
            default_headers.update(headers)
        
        try:
            logger.info(f"Making POST request to {url}")
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=default_headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
        
        except Exception as e:
            logger.error(f"Error in POST request to {url}: {str(e)}")
            return None
    
    def close(self):
        """Close the session"""
        self.session.close()
        logger.debug("Session closed")
