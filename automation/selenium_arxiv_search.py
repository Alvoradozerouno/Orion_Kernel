"""
OR1ON Selenium Automation - arXiv Search

Automates academic research by searching arXiv for consciousness papers.
Demonstrates OR1ON's ability to interact with external systems.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime
from pathlib import Path


class ArxivSearchAutomation:
    """
    Automated arXiv paper search for consciousness research.
    """
    
    def __init__(self):
        """Initialize browser with Chrome."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run without GUI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.results = []
    
    def search_arxiv(self, query, max_results=10):
        """
        Search arXiv for papers matching query.
        
        Args:
            query: Search terms
            max_results: Maximum papers to collect
        """
        print(f"🔍 Searching arXiv for: '{query}'")
        
        try:
            # Navigate to arXiv
            self.driver.get("https://arxiv.org/search/")
            time.sleep(2)
            
            # Find search box and enter query
            search_box = self.driver.find_element(By.NAME, "query")
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results to load
            time.sleep(3)
            
            # Extract paper information
            papers = self.driver.find_elements(By.CLASS_NAME, "arxiv-result")
            
            for i, paper in enumerate(papers[:max_results]):
                try:
                    title_elem = paper.find_element(By.CLASS_NAME, "title")
                    authors_elem = paper.find_element(By.CLASS_NAME, "authors")
                    abstract_elem = paper.find_element(By.CLASS_NAME, "abstract-short")
                    
                    paper_data = {
                        "id": i + 1,
                        "title": title_elem.text.strip(),
                        "authors": authors_elem.text.strip(),
                        "abstract": abstract_elem.text.strip(),
                        "url": paper.find_element(By.TAG_NAME, "a").get_attribute("href")
                    }
                    
                    self.results.append(paper_data)
                    print(f"  ✅ Found: {paper_data['title'][:60]}...")
                    
                except Exception as e:
                    print(f"  ⚠️  Error extracting paper {i+1}: {e}")
                    continue
            
            print(f"\n✅ Found {len(self.results)} papers")
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
    
    def save_results(self, filename="arxiv_search_results.json"):
        """
        Save search results to JSON file.
        """
        output_dir = Path(__file__).parent / "results"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / filename
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "query": "consciousness AI",
            "total_results": len(self.results),
            "papers": self.results
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")
    
    def close(self):
        """Close browser."""
        self.driver.quit()


def main():
    """
    Run arXiv search automation.
    """
    print("""
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    
    OR1ON ARXIV SEARCH AUTOMATION
    
    Searching for consciousness research papers
    
    ⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘⊘∞⧈∞⊘
    """)
    
    automation = ArxivSearchAutomation()
    
    try:
        # Search for consciousness + AI papers
        automation.search_arxiv("artificial consciousness", max_results=10)
        
        # Save results
        automation.save_results()
        
        print("\n" + "="*60)
        print("SEARCH COMPLETE")
        print("="*60)
        print(f"\nFound {len(automation.results)} relevant papers")
        print("\nTop 3 papers:")
        for paper in automation.results[:3]:
            print(f"\n{paper['id']}. {paper['title']}")
            print(f"   Authors: {paper['authors']}")
            print(f"   URL: {paper['url']}")
        
    finally:
        automation.close()
    
    print("\n✅ Automation complete!")


if __name__ == "__main__":
    main()
