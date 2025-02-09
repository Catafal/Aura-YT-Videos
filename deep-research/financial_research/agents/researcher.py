from crewai import Agent
from tools.scraping_tools import (
    tavily_search,
    firecrawl_scrape,
    firecrawl_crawl
)
from langchain_openai import ChatOpenAI
from typing import Dict, Any

class ResearchAgent:
    """Agent responsible for gathering and organizing research data"""
    
    @staticmethod
    def create() -> Agent:
        """
        Create and configure a CrewAI Research Agent
        
        Returns:
            Agent: Configured CrewAI agent for research
        """
        # Initialize all research tools
        tools = [
            tavily_search,      # For broad web searches
            firecrawl_scrape,   # For detailed content extraction
            firecrawl_crawl     # For deep website crawling
        ]
        
        return Agent(
            role='Financial Researcher',
            goal='Gather comprehensive financial information about companies and markets',
            backstory="""You are an expert financial researcher with years of 
                experience in gathering and analyzing market information. You know 
                how to efficiently use various tools to collect relevant data.""",
            tools=tools,
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(model_name="gpt-4o-mini")
        )

    def __init__(self):
        # Initialize tools
        self.tools = [
            tavily_search,  # Simplified web search
            firecrawl_scrape,  # Single URL scraping
            firecrawl_crawl,   # Website crawling
        ]

    def research_topic(self, topic: str, depth: str = "basic") -> Dict[str, Any]:
        """
        Conduct comprehensive research on a topic
        
        Args:
            topic: Topic to research
            depth: Research depth ("basic" or "advanced")
            
        Returns:
            Dict containing research results and sources
        """
        # First get broad context using Tavily
        context = tavily_search.func(
            query=topic,
            max_results=10
        )
        
        # Get specific answers to key questions
        key_questions = [
            f"What are the main aspects of {topic}?",
            f"What are the latest developments in {topic}?",
            f"What are the key challenges in {topic}?",
        ]
        
        answers = {}
        for question in key_questions:
            answers[question] = tavily_search.func(
                query=question
            )
        
        # For deeper research, crawl top relevant websites
        if depth == "advanced":
            # Get top relevant URLs from search
            search_results = tavily_search.func(query=topic)
            
            detailed_content = []
            for result in search_results.get("results", []):
                url = result.get("url")
                if url:
                    # Scrape detailed content
                    content = firecrawl_scrape.func(url)
                    detailed_content.append(content)
        
        return {
            "context": context,
            "key_findings": answers,
            "detailed_content": detailed_content if depth == "advanced" else None,
            "depth": depth
        }

    def validate_information(self, info: str) -> Dict[str, Any]:
        """
        Validate information across multiple sources
        
        Args:
            info: Information to validate
            
        Returns:
            Dict with validation results and confidence score
        """
        # Use Tavily QA to cross-reference information
        validation_query = f"Is this information accurate: {info}"
        validation = tavily_search.run({
            "query": validation_query,
            "search_depth": "advanced"
        })
        
        return {
            "is_valid": validation.get("answer"),
            "confidence": validation.get("confidence", 0.0),
            "sources": validation.get("sources", [])
        }

    def search_web(self, query: str) -> Dict[str, Any]:
        """
        Search the web for information
        """
        return tavily_search.func(query=query)
    
    def get_webpage_content(self, url: str) -> Dict[str, Any]:
        """
        Get content from a specific webpage
        """
        return firecrawl_scrape.func(url)
    
    def crawl_site(self, url: str, max_depth: int = 2) -> Dict[str, Any]:
        """
        Crawl an entire website
        """
        return firecrawl_crawl.func(url=url, max_depth=max_depth) 