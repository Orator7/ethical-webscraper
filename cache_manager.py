"""
Cache management to avoid redundant requests
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from logger import get_logger
from config import CACHE_ENABLED, CACHE_DURATION, CACHE_DIR

logger = get_logger()

class CacheManager:
    def __init__(self, enabled=CACHE_ENABLED, duration=CACHE_DURATION, cache_dir=CACHE_DIR):
        """
        Initialize cache manager
        
        Args:
            enabled: Whether caching is enabled
            duration: Cache duration in seconds
            cache_dir: Directory to store cache files
        """
        self.enabled = enabled
        self.duration = duration
        self.cache_dir = cache_dir
        
        if self.enabled:
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_key(self, url):
        """Generate a unique cache key for a URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _get_cache_path(self, url):
        """Get the file path for cached content"""
        cache_key = self._get_cache_key(url)
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, url):
        """
        Retrieve cached content if available and not expired
        
        Args:
            url: The URL to retrieve cache for
            
        Returns:
            str: Cached content, or None if not available/expired
        """
        if not self.enabled:
            return None
        
        cache_path = self._get_cache_path(url)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if cache has expired
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > timedelta(seconds=self.duration):
                logger.debug(f"Cache expired for {url}")
                os.remove(cache_path)
                return None
            
            logger.info(f"Cache hit for {url}")
            return cache_data['content']
        
        except Exception as e:
            logger.error(f"Error reading cache for {url}: {str(e)}")
            return None
    
    def set(self, url, content):
        """
        Store content in cache
        
        Args:
            url: The URL being cached
            content: The content to cache
        """
        if not self.enabled:
            return
        
        cache_path = self._get_cache_path(url)
        
        try:
            cache_data = {
                'url': url,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
            
            logger.debug(f"Cached content for {url}")
        
        except Exception as e:
            logger.error(f"Error writing cache for {url}: {str(e)}")
    
    def clear(self):
        """Clear all cached content"""
        if not self.enabled:
            return
        
        try:
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    os.remove(filepath)
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
