from langchain.tools import Tool
from typing import Dict, Any, Optional
import requests
from config.config import Config

# class SerperTool:
#     """Tool for performing web searches using Serper API"""
    
#     @staticmethod
#     def search(query: str) -> str:
#         """Execute a web search using Serper API"""
#         headers = {
#             "X-API-KEY": Config.SERPER_API_KEY,
#             "Content-Type": "application/json"
#         }
        
#         payload = {
#             "q": query,
#             "num": Config.MAX_SEARCH_RESULTS
#         }
        
#         response = requests.post(
#             "https://api.serper.dev/search",
#             headers=headers,
#             json=payload
#         )
        
#         return response.json()

# Create Tool instances using langchain's Tool
# serper_tool = Tool(
#     name='Serper Search',
#     description='Search the web using Serper API',
#     func=SerperTool.search
# )


class TavilySearchTool:
    """Simple tool for web searches using Tavily API"""
    
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.base_url = "https://api.tavily.com/search"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Execute a web search using Tavily API
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Dict containing search results
        """
        try:
            payload = {
                "query": query,
                "max_results": max_results,
                "include_answer": True
            }

            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "details": response.text
                }
                
            return response.json()
            
        except Exception as e:
            return {
                "error": "Request failed",
                "details": str(e)
            }

class FirecrawlTool:
    """Tool for web scraping and crawling using Firecrawl API"""
    
    def __init__(self):
        self.api_key = Config.FIRECRAWL_API_KEY
        self.base_url = "https://api.firecrawl.dev/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape content from a single URL
        
        Args:
            url: The URL to scrape
            
        Returns:
            Dict containing scraped content and metadata
        """
        try:
            response = requests.post(
                f"{self.base_url}/scrape",
                headers=self.headers,
                json={"url": url}
            )
            
            if response.status_code != 200:
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "details": response.text
                }
                
            return response.json()
            
        except Exception as e:
            return {
                "error": "Request failed", 
                "details": str(e)
            }

    def crawl_website(self, url: str, max_depth: Optional[int] = None) -> Dict[str, Any]:
        """
        Crawl a website starting from a URL
        
        Args:
            url: Starting URL to crawl
            max_depth: Maximum crawl depth (optional)
            
        Returns:
            Dict containing crawl results
        """
        payload = {"url": url}
        if max_depth:
            payload["maxDepth"] = max_depth

        try:
            response = requests.post(
                f"{self.base_url}/crawl",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "details": response.text
                }
                
            return response.json()
            
        except Exception as e:
            return {
                "error": "Request failed",
                "details": str(e)
            }

# Initialize tool instances
tavily = TavilySearchTool()
firecrawl = FirecrawlTool()

# Create Tool instances
tavily_search = Tool(
    name='Web Search',
    description='Search the web using Tavily API',
    func=tavily.search
)

firecrawl_scrape = Tool(
    name='Web Scraper',
    description='Scrape content from a single URL',
    func=firecrawl.scrape_url
)

firecrawl_crawl = Tool(
    name='Web Crawler',
    description='Crawl an entire website starting from a URL',
    func=firecrawl.crawl_website
)
