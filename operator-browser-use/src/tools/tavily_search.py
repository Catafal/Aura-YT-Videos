from tavily import TavilyClient
import os
from typing import Dict, List, Union

class TavilySearchTool:
    """
    A tool for performing web searches using the Tavily API to get relevant URLs.
    """
    def __init__(self):
        # Initialize Tavily client with API key from environment variable
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable is not set")
        self.client = TavilyClient(api_key=api_key)

    def get_relevant_urls(self, query: str, max_results: int = 3) -> List[str]:
        """
        Get the most relevant URLs for a given query.
        
        Args:
            query (str): The search query
            max_results (int): Maximum number of URLs to return
            
        Returns:
            List[str]: List of most relevant URLs
        """
        try:
            # Get search results
            response = self.client.search(
                query=query,
                search_depth="basic",
                include_answer=False,
                include_raw_content=False,
            )
            
            # Extract URLs from results
            urls = [result['url'] for result in response.get('results', [])[:max_results]]
            return urls
            
        except Exception as e:
            print(f"Tavily search error: {str(e)}")
            return []

    def search(self, query: str, search_depth: str = "basic") -> Union[str, Dict]:
        """
        Perform a web search using Tavily API.
        
        Args:
            query (str): The search query
            search_depth (str): Either "basic" (1 credit) or "advanced" (2 credits)
            
        Returns:
            Union[str, Dict]: Search results either as formatted string or raw dict
        """
        try:
            # Get search results
            response = self.client.search(
                query=query,
                search_depth=search_depth
            )
            return response
            
        except Exception as e:
            return f"Search error: {str(e)}"

    def get_quick_answer(self, query: str) -> str:
        """
        Get a quick answer to a question using Tavily's QnA search.
        
        Args:
            query (str): The question to answer
            
        Returns:
            str: A concise answer to the question
        """
        try:
            return self.client.qna_search(query=query)
        except Exception as e:
            return f"QnA search error: {str(e)}"