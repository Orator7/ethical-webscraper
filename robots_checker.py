"""
Check robots.txt compliance before scraping
"""

from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from logger import get_logger

logger = get_logger()

class RobotsChecker:
    def __init__(self):
        self.cache = {}
    
    def get_robots_url(self, url):
        """Extract the robots.txt URL from a given URL"""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        return robots_url
    
    def is_allowed(self, url, user_agent="*"):
        """
        Check if a URL is allowed according to robots.txt
        
        Args:
            url: The URL to check
            user_agent: The user agent to check against (default: *)
            
        Returns:
            bool: True if allowed, False otherwise
        """
        try:
            robots_url = self.get_robots_url(url)
            
            # Check cache
            if robots_url not in self.cache:
                rp = RobotFileParser()
                rp.set_url(robots_url)
                try:
                    rp.read()
                    self.cache[robots_url] = rp
                    logger.info(f"Loaded robots.txt from {robots_url}")
                except Exception as e:
                    logger.warning(f"Could not fetch robots.txt from {robots_url}: {str(e)}")
                    # If robots.txt doesn't exist, allow scraping
                    return True
            
            rp = self.cache[robots_url]
            
            if rp.can_fetch(user_agent, url):
                logger.debug(f"URL allowed by robots.txt: {url}")
                return True
            else:
                logger.warning(f"URL disallowed by robots.txt: {url}")
                return False
                
        except Exception as e:
            logger.error(f"Error checking robots.txt: {str(e)}")
            # Be conservative: if we can't check, assume not allowed
            return False
    
    def get_crawl_delay(self, url, user_agent="*"):
        """Get the crawl delay specified in robots.txt"""
        try:
            robots_url = self.get_robots_url(url)
            
            if robots_url not in self.cache:
                self.is_allowed(url, user_agent)
            
            rp = self.cache.get(robots_url)
            if rp:
                delay = rp.request_rate(user_agent)
                if delay:
                    return delay.requests / delay.seconds
        except Exception as e:
            logger.error(f"Error getting crawl delay: {str(e)}")
        
        return None
