"""
Manage caching of scraped content
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from logger import get_logger
from config import CACHE_ENABLED, CACHE_DURATION

logger = get_logger()

class CacheManager:
    def __init__(self, cache_dir='cache'):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = cache_dir
        self.enabled = CACHE_ENABLED
        self.duration = CACHE_DURATION
        
        # Create cache directory if it doesn't exist
        if self.enabled and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
            logger.info(f"Created cache directory: {cache_dir}")
    
    def _get_cache_key(self, url):
        """Generate cache key from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _get_cache_file(self, url):
        """Get cache file path"""
        key = self._get_cache_key(url)
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, url):
        """
        Get cached content if available and not expired
        
        Args:
            url: URL to check cache for
            
        Returns:
            Cached content or None
        """
        if not self.enabled:
            return None
        
        try:
            cache_file = self._get_cache_file(url)
            
            if not os.path.exists(cache_file):
                return None
            
            # Check if cache is expired
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache_file))
            
            if file_age > timedelta(seconds=self.duration):
                logger.debug(f"Cache expired for {url}")
                os.remove(cache_file)
                return None
            
            # Read cached content
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"Cache hit for {url}")
                return data['content']
                
        except Exception as e:
            logger.warning(f"Error reading cache: {str(e)}")
            return None
    
    def set(self, url, content):
        """
        Cache content for a URL
        
        Args:
            url: URL to cache for
            content: Content to cache
        """
        if not self.enabled:
            return
        
        try:
            cache_file = self._get_cache_file(url)
            
            data = {
                'url': url,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
                logger.debug(f"Cached content for {url}")
                
        except Exception as e:
            logger.warning(f"Error writing cache: {str(e)}")
    
    def clear(self):
        """Clear all cache files"""
        try:
            if os.path.exists(self.cache_dir):
                for file in os.listdir(self.cache_dir):
                    os.remove(os.path.join(self.cache_dir, file))
                logger.info("Cache cleared")
        except Exception as e:
            logger.warning(f"Error clearing cache: {str(e)}")
