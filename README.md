# Ethical Web Scraper 🕷️

A powerful, responsible web scraper framework that respects `robots.txt`, implements rate limiting, and handles errors gracefully. Built for ethical scraping practices.

## 🎯 Features

✅ **Robots.txt Compliance** - Automatically checks and respects `robots.txt`  
✅ **Rate Limiting** - Polite delays between requests to avoid overloading servers  
✅ **Caching** - Smart caching to reduce redundant requests  
✅ **Error Handling** - Robust retry logic with exponential backoff  
✅ **Flexible Parsing** - Extract data using CSS selectors or custom logic  
✅ **Logging** - Comprehensive logging for debugging  
✅ **Multi-site Support** - Site-specific configurations  
✅ **Easy to Use** - Simple, intuitive API  

---

## ⚙️ Setup & Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/Orator7/ethical-webscraper.git
cd ethical-webscraper
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Configure Environment (Optional)**
```bash
cp .env.example .env
# Edit .env if needed (logging level, proxy settings, etc.)
```

---

## 🚀 How to Use in VS Code

### Step 1: Open VS Code
1. Open VS Code
2. Open your project folder: `File → Open Folder` → Select `ethical-webscraper`

### Step 2: Create a Python Script
1. Right-click in the explorer → **New File**
2. Name it `my_scraper.py`
3. Add this basic code:

```python
from scraper import EthicalWebScraper

# Create scraper instance
scraper = EthicalWebScraper()

# Scrape a website
url = "https://example.com"
content = scraper.scrape(url)

if content:
    print("✓ Successfully scraped!")
    print(f"Content length: {len(content)} characters")
else:
    print("✗ Failed to scrape")

scraper.close()
```

### Step 3: Run Your Script
1. **Option A - Using VS Code Terminal:**
   - Press `Ctrl + ` (backtick) to open terminal
   - Type: `python my_scraper.py`
   - Press Enter

2. **Option B - Using Run Button:**
   - Click the ▶️ **Run** button (top right)
   - Select **Run Python File**

---

## 📚 Complete Usage Examples

### Example 1: Basic Scraping
```python
from scraper import EthicalWebScraper

scraper = EthicalWebScraper()

# Simple scrape
url = "https://example.com"
html = scraper.scrape(url)

if html:
    print(f"Scraped {len(html)} characters")

scraper.close()
```

### Example 2: Parse & Extract Data
```python
from scraper import EthicalWebScraper

scraper = EthicalWebScraper()

# Scrape and parse in one step
url = "https://example.com"
parser = scraper.scrape_and_parse(url)

if parser:
    # Extract different data types
    title = parser.get_title()
    links = parser.extract_links()
    images = parser.extract_images()
    
    print(f"Title: {title}")
    print(f"Found {len(links)} links")
    print(f"Found {len(images)} images")
    
    # Print first 3 links
    for link in links[:3]:
        print(f"  - {link['text']}: {link['href']}")

scraper.close()
```

### Example 3: Search for Keyword
```python
from scraper import EthicalWebScraper

scraper = EthicalWebScraper()

# Search keyword across multiple sites
keyword = "contact"
urls = [
    "https://example.com",
    "https://example.org",
]

results = scraper.search_keyword(keyword, urls)

for url, found in results.items():
    status = "✓ FOUND" if found else "✗ NOT FOUND"
    print(f"{url}: {status}")

scraper.close()
```

### Example 4: Extract Specific Data with CSS Selectors
```python
from scraper import EthicalWebScraper

scraper = EthicalWebScraper()

url = "https://example.com"

# Define what you want to extract
selectors = {
    'headings': 'h1, h2, h3',
    'paragraphs': 'p',
    'links': 'a[href]',
}

data = scraper.extract_data(url, selectors)

if data:
    print(f"Headings: {len(data.get('headings', []))} found")
    print(f"Paragraphs: {len(data.get('paragraphs', []))} found")
    print(f"Links: {len(data.get('links', []))} found")

scraper.close()
```

### Example 5: Check robots.txt Compliance
```python
from scraper import EthicalWebScraper

scraper = EthicalWebScraper()

# Check if URL can be scraped
url = "https://example.com/page"
allowed = scraper.robots_checker.is_allowed(url)

if allowed:
    print(f"✓ {url} is allowed by robots.txt")
else:
    print(f"✗ {url} is disallowed by robots.txt")

scraper.close()
```

### Example 6: Custom HTML Parsing
```python
from scraper import EthicalWebScraper

scraper = EthicalWebScraper()

url = "https://example.com"
parser = scraper.scrape_and_parse(url)

if parser:
    # Extract custom elements
    divs = parser.find_by_selector('div.content')
    print(f"Found {len(divs)} content divs")
    
    # Extract specific attributes
    links_with_title = parser.extract_custom('a', attribute='title')
    print(f"Links with titles: {links_with_title[:5]}")
    
    # Get all text
    text = parser.get_text()
    print(f"Page text ({len(text)} chars): {text[:200]}...")

scraper.close()
```

---

## 📋 Project Structure

```
ethical-webscraper/
├── scraper.py              # Main scraper class
├── parser.py               # HTML parsing utilities
├── request_handler.py      # HTTP requests with retries
├── rate_limiter.py         # Rate limiting (be polite!)
├── robots_checker.py       # robots.txt compliance
├── cache_manager.py        # Response caching
├── config.py               # Configuration settings
├── logger.py               # Logging setup
├── examples.py             # Complete usage examples
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration
└── README.md               # This file
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Request timeout (seconds)
DEFAULT_TIMEOUT = 10

# Retry attempts
DEFAULT_RETRIES = 3

# Delay between requests (seconds)
DEFAULT_DELAY_BETWEEN_REQUESTS = 2

# Max requests per minute
DEFAULT_REQUESTS_PER_MINUTE = 20

# Enable/disable caching
CACHE_ENABLED = True

# Cache duration (1 hour)
CACHE_DURATION = 3600
```

### Site-Specific Config
```python
SITE_CONFIGS = {
    "example.com": {
        "delay": 3,
        "requests_per_minute": 10,
        "timeout": 15,
    }
}
```

---

## 🛡️ Ethical Scraping Guidelines

✅ **DO:**
- Respect `robots.txt`
- Use appropriate delays
- Identify yourself with a proper User-Agent
- Cache responses when possible
- Only scrape what you need
- Check the website's ToS

❌ **DON'T:**
- Ignore `robots.txt`
- Hammer servers with rapid requests
- Scrape personal/sensitive data
- Bypass authentication
- Violate copyright
- Republish content without permission

---

## 🔍 Debugging

### View Logs
Logs are saved in `logs/scraper.log` and displayed in console.

### Change Log Level
In `.env`:
```
LOG_LEVEL=DEBUG
```

### Common Issues

**Issue: "robots.txt disallowed"**
- Solution: Check if the site allows scraping in robots.txt
- Use: `scraper.robots_checker.is_allowed(url)`

**Issue: Timeout errors**
- Solution: Increase timeout in `config.py`
- Or: `DEFAULT_TIMEOUT = 30`

**Issue: Too many requests**
- Solution: Increase delay between requests
- Or: `DEFAULT_DELAY_BETWEEN_REQUESTS = 5`

---

## 📦 Dependencies

- `requests` - HTTP library
- `beautifulsoup4` - HTML parsing
- `selenium` - JavaScript rendering (optional)
- `lxml` - XML/HTML parser
- `urllib3` - HTTP client
- `python-dotenv` - Environment variables

---

## 📝 License

MIT License - Use responsibly and ethically!

---

## 🤝 Contributing

Have improvements? Submit a pull request or open an issue!

---

## ⚠️ Legal Notice

**This tool is for educational and legitimate purposes only.**

- Always obtain permission before scraping
- Respect copyright and data protection laws (GDPR, CCPA, etc.)
- Follow the website's Terms of Service
- Don't use for malicious purposes
- Be ethical and responsible

The author is not responsible for misuse of this tool.

---

## 🎓 Learn More

- [robots.txt Specification](https://www.robotstxt.org/)
- [Web Scraping Best Practices](https://en.wikipedia.org/wiki/Web_scraping#Legal_and_ethical_issues)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Docs](https://requests.readthedocs.io/)

---

**Happy scraping! 🕷️** Remember to always scrape responsibly and ethically.
