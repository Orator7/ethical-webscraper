"""
Web scraper with results saved to Word document
"""

from scraper import EthicalWebScraper
from docx import Document
from docx.shared import Pt, RGBColor
from datetime import datetime

def save_to_word(results, file_path):
    """Save scraping results to a Word document"""
    
    # Create or open document
    try:
        doc = Document(file_path)
        print(f"✓ Opened existing file: {file_path}")
    except:
        doc = Document()
        print(f"✓ Created new file: {file_path}")
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add title
    title = doc.add_heading(f'Web Scraping Results', 0)
    title.runs[0].font.color.rgb = RGBColor(0, 51, 102)
    
    # Add timestamp
    timestamp_para = doc.add_paragraph(f"Generated: {timestamp}")
    timestamp_para.runs[0].font.italic = True
    timestamp_para.runs[0].font.size = Pt(10)
    
    doc.add_paragraph()  # Blank line
    
    # Add results
    for key, value in results.items():
        # Add section heading
        heading = doc.add_heading(key, level=1)
        heading.runs[0].font.color.rgb = RGBColor(0, 102, 204)
        
        # Add content
        if isinstance(value, list):
            for item in value:
                doc.add_paragraph(str(item), style='List Bullet')
        elif isinstance(value, dict):
            for k, v in value.items():
                doc.add_paragraph(f"{k}: {v}")
        else:
            doc.add_paragraph(str(value))
        
        doc.add_paragraph()  # Blank line
    
    # Save document
    doc.save(file_path)
    print(f"✓ Results saved to: {file_path}")

def scrape_and_save(url, output_file):
    """Scrape website and save results to Word document"""
    
    scraper = EthicalWebScraper()
    results = {}
    
    print("=" * 60)
    print(f"SCRAPING: {url}")
    print("=" * 60)
    
    # ===== EXAMPLE 1: Basic Scraping =====
    print("\n[1/6] Basic Scraping...")
    content = scraper.scrape(url)
    
    if content:
        print(f"✓ Successfully scraped {url}")
        results['1. Basic Info'] = {
            'URL': url,
            'Content Length': f"{len(content)} characters",
            'Status': '✓ Success'
        }
    else:
        print(f"✗ Failed to scrape {url}")
        results['1. Basic Info'] = {
            'URL': url,
            'Status': '✗ Failed'
        }
        scraper.close()
        return results
    
    # ===== EXAMPLE 2: Parse and Extract Links =====
    print("[2/6] Extracting links...")
    parser = scraper.scrape_and_parse(url)
    
    if parser:
        links = parser.extract_links()
        results['2. Links Found'] = [
            f"{link['text'][:50]} → {link['href'][:70]}" 
            for link in links[:10]
        ]
        print(f"✓ Found {len(links)} links (showing first 10)")
    else:
        print("✗ Could not parse page")
        results['2. Links Found'] = ["Failed to parse"]
    
    # ===== EXAMPLE 3: Extract Images =====
    print("[3/6] Extracting images...")
    if parser:
        images = parser.extract_images()
        results['3. Images Found'] = [
            f"[Alt: {img['alt'][:40]}] → {img['src'][:70]}" 
            for img in images[:10]
        ]
        print(f"✓ Found {len(images)} images (showing first 10)")
    else:
        results['3. Images Found'] = ["Failed to extract"]
    
    # ===== EXAMPLE 4: Extract Tables =====
    print("[4/6] Extracting tables...")
    if parser:
        tables = parser.extract_tables()
        table_info = []
        for i, table in enumerate(tables[:3], 1):
            table_info.append(f"Table {i}: {len(table)} rows")
        results['4. Tables Found'] = table_info if table_info else ["No tables found"]
        print(f"✓ Found {len(tables)} tables")
    else:
        results['4. Tables Found'] = ["Failed to extract"]
    
    # ===== EXAMPLE 5: Extract Metadata =====
    print("[5/6] Extracting metadata...")
    if parser:
        metadata = parser.extract_metadata()
        meta_info = []
        for key, value in list(metadata.items())[:10]:
            meta_info.append(f"{key}: {value[:60]}")
        results['5. Meta Tags'] = meta_info if meta_info else ["No metadata found"]
        print(f"✓ Found {len(metadata)} meta tags")
    else:
        results['5. Meta Tags'] = ["Failed to extract"]
    
    # ===== EXAMPLE 6: Page Title =====
    print("[6/6] Extracting page title...")
    if parser:
        title = parser.get_title()
        results['6. Page Title'] = title if title else "No title found"
        print(f"✓ Title: {title}")
    else:
        results['6. Page Title'] = "Failed to extract"
    
    scraper.close()
    
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETED!")
    print("=" * 60)
    
    return results

def main():
    """Main execution function"""
    
    # Configuration
    url = "https://example.com"  # Change this to your target URL
    output_file = r"D:\Code\Scraper Result.docx"  # Your Word file path
    
    print("🕷️  ETHICAL WEB SCRAPER WITH WORD EXPORT")
    print("=" * 60)
    
    try:
        # Scrape the website
        results = scrape_and_save(url, output_file)
        
        # Save to Word document
        print(f"\n📄 Saving results to Word document...")
        save_to_word(results, output_file)
        
        print("\n" + "=" * 60)
        print("✓ ALL DONE!")
        print(f"📄 Results saved to: {output_file}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("Make sure:")
        print("  1. You have 'python-docx' installed: pip install python-docx")
        print("  2. The directory D:\\Code\\ exists")
        print("  3. The file path is correct")

if __name__ == "__main__":
    main()
