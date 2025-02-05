import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the financial research project"""
    
    # API Keys
    SERPER_API_KEY = os.getenv('SERPER_API_KEY')
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
    APIFY_API_KEY = os.getenv('APIFY_API_KEY')
    FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
    
    # Model configurations
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEFAULT_MODEL = "deepseek-r1:14b"  # Can be switched to o3-mini as needed
    
    # Tool configurations
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', '10'))
    SEARCH_TIMEOUT = 30  # seconds 