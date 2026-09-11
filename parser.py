"""
Parse HTML content and extract data
"""

from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger()

class Parser:
    def __init__(self, content, parser='html.parser'):
        """
        Initialize parser
        
        Args:
            content: HTML content to parse
            parser: BeautifulSoup parser type
        """
        self.content = content
        self.soup = BeautifulSoup(content, parser)
    
    def get_title(self):
        """Extract page title"""
        try:
            title = self.soup.title
            return title.string if title else None
        except Exception as e:
            logger.error(f"Error extracting title: {str(e)}")
            return None
    
    def get_text(self):
        """Extract all text from page"""
        try:
            return self.soup.get_text(strip=True)
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return None
    
    def find_by_selector(self, selector):
        """
        Find elements by CSS selector
        
        Args:
            selector: CSS selector string
            
        Returns:
            list: List of matching elements
        """
        try:
            return self.soup.select(selector)
        except Exception as e:
            logger.error(f"Error with selector '{selector}': {str(e)}")
            return []
    
    def find_by_tag(self, tag, **kwargs):
        """
        Find elements by tag name
        
        Args:
            tag: HTML tag name
            **kwargs: Additional attributes to match
            
        Returns:
            list: List of matching elements
        """
        try:
            return self.soup.find_all(tag, **kwargs)
        except Exception as e:
            logger.error(f"Error finding tag '{tag}': {str(e)}")
            return []
    
    def extract_links(self):
        """Extract all links from page"""
        try:
            links = []
            for link in self.soup.find_all('a', href=True):
                links.append({
                    'text': link.get_text(strip=True),
                    'href': link['href']
                })
            logger.debug(f"Extracted {len(links)} links")
            return links
        except Exception as e:
            logger.error(f"Error extracting links: {str(e)}")
            return []
    
    def extract_metadata(self):
        """Extract meta tags"""
        try:
            metadata = {}
            for meta in self.soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    metadata[name] = content
            logger.debug(f"Extracted {len(metadata)} meta tags")
            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            return {}
    
    def extract_tables(self):
        """Extract tables from page"""
        try:
            tables = []
            for table in self.soup.find_all('table'):
                rows = []
                for tr in table.find_all('tr'):
                    cols = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                    if cols:
                        rows.append(cols)
                if rows:
                    tables.append(rows)
            logger.debug(f"Extracted {len(tables)} tables")
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables: {str(e)}")
            return []
    
    def extract_images(self):
        """Extract images from page"""
        try:
            images = []
            for img in self.soup.find_all('img'):
                images.append({
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
            logger.debug(f"Extracted {len(images)} images")
            return images
        except Exception as e:
            logger.error(f"Error extracting images: {str(e)}")
            return []
    
    def extract_custom(self, selector, attribute=None):
        """
        Extract custom data using CSS selector
        
        Args:
            selector: CSS selector
            attribute: Optional attribute to extract (default: text content)
            
        Returns:
            list: Extracted data
        """
        try:
            elements = self.find_by_selector(selector)
            data = []
            for elem in elements:
                if attribute:
                    value = elem.get(attribute)
                else:
                    value = elem.get_text(strip=True)
                if value:
                    data.append(value)
            return data
        except Exception as e:
            logger.error(f"Error extracting custom data: {str(e)}")
            return []
