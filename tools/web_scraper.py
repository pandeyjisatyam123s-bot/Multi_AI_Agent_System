from bs4 import BeautifulSoup
import requests
from langchain_core.tools import Tool

def scrape_webpage(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:5000] # Limit to 5000 chars to avoid context overflow
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

def get_scraper_tool() -> Tool:
    return Tool(
        name="web_scraper",
        description="Scrape text content from a given URL.",
        func=scrape_webpage
    )
