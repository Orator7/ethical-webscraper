"""
Main web scraper class that orchestrates all components
"""

from urllib.parse import urlparse
from logger import get_logger
from robots_checker import RobotsChecker
from rate_limiter import RateLimiter
from cache_manager import CacheManager
from request_handler import RequestHandler
from parser import Parser
from config import SITE_CONFIGS, DEFAULT_USER_AGENT

logger = get_logger()

class EthicalWebScraper:
    def __init__(self):
        """Initialize the ethical web scraper"""
        self.robots_checker = RobotsChecker()
        self.rate_limiter = RateLimiter()
        self.cache_manager = CacheManager()
        self.request_handler = RequestHandler()
    
    def _get_domain(self, url):
        """Extract domain from URL"""
        parsed = urlparse(url)
        return parsed.netloc
    
    def _get_site_config(self, domain):
        """Get configuration for a specific site"""
        if domain in SITE_CONFIGS:
            return SITE_CONFIGS[domain]
        return SITE_CONFIGS.get("default", {})
    
    def scrape(self, url, use_cache=True, user_agent=None):
        """
        Main scraping function
        
        Args:
            url: URL to scrape
            use_cache: Whether to use cached content
            user_agent: Optional custom user agent
            
        Returns:
            str: HTML content or None on failure
        """
        logger.info(f"Starting scrape of {url}")
        
        domain = self._get_domain(url)
        config = self._get_site_config(domain)
        
        # Apply site-specific configuration
        if config != SITE_CONFIGS.get("default"):
            self.rate_limiter.set_limits(
                domain,
                config.get("delay", 2),
                config.get("requests_per_minute", 20)
            )
        
        # Check if scraping is allowed by robots.txt
        if not self.robots_checker.is_allowed(url, user_agent or DEFAULT_USER_AGENT):
            logger.error(f"Scraping disallowed by robots.txt: {url}")
            return None
        
        # Check cache
        if use_cache:
            cached_content = self.cache_manager.get(url)
            if cached_content:
                return cached_content
        
        # Apply rate limiting
        self.rate_limiter.wait(domain)
        
        # Make request
        response = self.request_handler.get(url, timeout=config.get("timeout", 10))
        
        if response is None or response.status_code != 200:
            logger.error(f"Failed to retrieve {url}")
            return None
        
        content = response.text
        
        # Cache the content
        self.cache_manager.set(url, content)
        
        logger.info(f"Successfully scraped {url}")
        return content
    
    def scrape_and_parse(self, url, use_cache=True):
        """
        Scrape a URL and return a Parser object
        
        Args:
            url: URL to scrape
            use_cache: Whether to use cached content
            
        Returns:
            Parser: Parser object or None on failure
        """
        content = self.scrape(url, use_cache=use_cache)
        
        if content is None:
            return None
        
        return Parser(content)
    
    def search_keyword(self, keyword, urls):
        """
        Search for a keyword across multiple URLs
        
        Args:
            keyword: Keyword to search for
            urls: List of URLs to search
            
        Returns:
            dict: Results with URL as key and boolean indicating if keyword found
        """
        results = {}
        logger.info(f"Searching for '{keyword}' across {len(urls)} URLs")
        
        for url in urls:
            parser = self.scrape_and_parse(url)
            if parser:
                text = parser.get_text()
                results[url] = keyword.lower() in text.lower()
                logger.debug(f"'{keyword}' found: {results[url]}")
            else:
                results[url] = False
        
        return results
    
    def extract_data(self, url, selectors):
        """
        Extract specific data from a URL using CSS selectors
        
        Args:
            url: URL to scrape
            selectors: Dict of {name: css_selector}
            
        Returns:
            dict: Extracted data
        """
        parser = self.scrape_and_parse(url)
        
        if parser is None:
            return None
        
        data = {}
        for name, selector in selectors.items():
            data[name] = parser.extract_custom(selector)
        
        logger.debug(f"Extracted data from {url}: {data}")
        return data
    
    def close(self):
        """Close all connections and cleanup"""
        self.request_handler.close()
        logger.info("Scraper closed")
