"""
Example usage of the ethical web scraper
"""

from scraper import EthicalWebScraper
from logger import get_logger
import json

logger = get_logger()

def example_1_basic_scrape():
    """Example 1: Basic scraping"""
    print("\n" + "="*50)
    print("EXAMPLE 1: Basic Scraping")
    print("="*50)
    
    scraper = EthicalWebScraper()
    
    # Scrape a website
    url = "https://example.com"
    content = scraper.scrape(url)
    
    if content:
        print(f"Successfully scraped {url}")
        print(f"Content length: {len(content)} characters")
    else:
        print(f"Failed to scrape {url}")
    
    scraper.close()


def example_2_parse_and_extract():
    """Example 2: Parse HTML and extract specific elements"""
    print("\n" + "="*50)
    print("EXAMPLE 2: Parse and Extract Data")
    print("="*50)
    
    scraper = EthicalWebScraper()
    
    # Scrape and parse in one step
    url = "https://example.com"
    parser = scraper.scrape_and_parse(url)
    
    if parser:
        # Extract various data
        title = parser.get_title()
        links = parser.extract_links()
        metadata = parser.extract_metadata()
        
        print(f"Title: {title}")
        print(f"Found {len(links)} links")
        print(f"Metadata: {json.dumps(metadata, indent=2)}")
        
        # Print first 3 links
        print("\nFirst 3 links:")
        for link in links[:3]:
            print(f"  - {link['text']}: {link['href']}")
    
    scraper.close()


def example_3_search_keyword():
    """Example 3: Search for keyword across multiple sites"""
    print("\n" + "="*50)
    print("EXAMPLE 3: Search Keyword Across Sites")
    print("="*50)
    
    scraper = EthicalWebScraper()
    
    keyword = "contact"
    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    results = scraper.search_keyword(keyword, urls)
    
    print(f"\nSearching for '{keyword}':")
    for url, found in results.items():
        status = "✓ FOUND" if found else "✗ NOT FOUND"
        print(f"  {url}: {status}")
    
    scraper.close()


def example_4_extract_specific_data():
    """Example 4: Extract specific data using CSS selectors"""
    print("\n" + "="*50)
    print("EXAMPLE 4: Extract Specific Data with CSS Selectors")
    print("="*50)
    
    scraper = EthicalWebScraper()
    
    url = "https://example.com"
    
    # Define CSS selectors for data you want to extract
    selectors = {
        'headings': 'h1, h2, h3',
        'paragraphs': 'p',
        'links': 'a',
    }
    
    data = scraper.extract_data(url, selectors)
    
    if data:
        print(f"\nExtracted data from {url}:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed to extract data from {url}")
    
    scraper.close()


def example_5_robots_check():
    """Example 5: Check robots.txt compliance"""
    print("\n" + "="*50)
    print("EXAMPLE 5: Check Robots.txt Compliance")
    print("="*50)
    
    scraper = EthicalWebScraper()
    
    test_urls = [
        "https://example.com",
        "https://example.org/robots.txt",
    ]
    
    print("\nChecking robots.txt compliance:")
    for url in test_urls:
        allowed = scraper.robots_checker.is_allowed(url)
        status = "✓ ALLOWED" if allowed else "✗ DISALLOWED"
        print(f"  {url}: {status}")
    
    scraper.close()


def example_6_custom_parsing():
    """Example 6: Custom HTML parsing"""
    print("\n" + "="*50)
    print("EXAMPLE 6: Custom HTML Parsing")
    print("="*50)
    
    scraper = EthicalWebScraper()
    
    url = "https://example.com"
    parser = scraper.scrape_and_parse(url)
    
    if parser:
        # Extract multiple types of data
        print(f"\nData extracted from {url}:")
        
        title = parser.get_title()
        print(f"  Title: {title}")
        
        images = parser.extract_images()
        print(f"  Images found: {len(images)}")
        if images:
            print(f"    First image: {images[0]}")
        
        tables = parser.extract_tables()
        print(f"  Tables found: {len(tables)}")
        
        # Extract custom data using CSS selector
        custom_data = parser.extract_custom('div.content')
        print(f"  Custom divs with 'content' class: {len(custom_data)}")
    
    scraper.close()


if __name__ == "__main__":
    """
    USAGE GUIDE:
    
    1. Uncomment the example you want to run
    2. Update URLs to real websites you want to test
    3. Make sure you have permission to scrape those sites
    4. Run: python examples.py
    """
    
    # Uncomment the examples you want to run:
    example_1_basic_scrape()
    example_2_parse_and_extract()
    example_3_search_keyword()
    example_4_extract_specific_data()
    example_5_robots_check()
    example_6_custom_parsing()
    
    print("\n" + "="*50)
    print("All examples completed!")
    print("="*50)
