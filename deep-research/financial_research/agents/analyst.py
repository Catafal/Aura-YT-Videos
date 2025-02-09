from crewai import Agent, LLM
from tools.scraping_tools import (
    tavily_search
)
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List

class AnalystAgent:
    """Agent responsible for analyzing research data and generating insights"""
    
    @staticmethod
    def create() -> Agent:
        """
        Create and configure a CrewAI Analyst Agent
        
        Returns:
            Agent: Configured CrewAI agent for analysis
        """
        # Initialize analysis tools
        tools = [
            tavily_search,     # For fact-checking and updates
        ]
        
        return Agent(
            role='Financial Analyst',
            goal='Analyze financial data and provide actionable insights',
            backstory="""You are a seasoned financial analyst with expertise in 
                evaluating market trends and investment opportunities. You excel at 
                interpreting complex data and providing clear, actionable insights.""",
            tools=tools,
            verbose=True,
            allow_delegation=True,
            # llm=ChatOpenAI(model_name="o3-mini")
            llm= LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434")
        )

    def __init__(self):
        # Initialize tools - analyst typically only needs search
        self.tools = [
            tavily_search,
        ]

    def analyze_research(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze research data and generate insights
        
        Args:
            research_data: Data from the research agent
            
        Returns:
            Dict containing analysis results and recommendations
        """
        # Get latest context for analysis
        context = research_data.get("context", "")
        topic = research_data.get("topic", "")
        
        # Verify and update information
        latest_updates = tavily_search.func(
            query=f"latest news and developments about {topic}",
            max_results=5
        )
        
        # Get specific insights through targeted questions
        analysis_questions = [
            f"What are the key trends in {topic}?",
            f"What are the potential implications of {topic}?",
            f"What are expert opinions on {topic}?"
        ]
        
        insights = {}
        for question in analysis_questions:
            insights[question] = tavily_search.func(
                query=question
            )
        
        return {
            "topic": topic,
            "latest_updates": latest_updates,
            "insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }

    def _generate_recommendations(self, insights: Dict[str, str]) -> List[str]:
        """Generate recommendations based on insights"""
        recommendations = []
        for insight in insights.values():
            if isinstance(insight, str):
                # Use LLM to extract actionable recommendations
                prompt = f"Based on this insight: {insight}\nWhat are the key recommendations?"
                response = self.llm.predict(prompt)
                recommendations.extend(response.split('\n'))
        return recommendations

    def fact_check(self, statement: str) -> Dict[str, Any]:
        """
        Perform fact-checking on a statement
        
        Args:
            statement: Statement to fact-check
            
        Returns:
            Dict with fact-check results and sources
        """
        # Use Tavily QA for fact-checking
        fact_check_query = f"Fact check: {statement}"
        result = tavily_search.run({
            "query": fact_check_query,
            "search_depth": "advanced",
            "include_answer": True
        })
        
        return {
            "statement": statement,
            "verification": result.get("answer"),
            "confidence": result.get("confidence", 0.0),
            "sources": result.get("sources", [])
        }

    def verify_information(self, claim: str) -> Dict[str, Any]:
        """
        Verify a piece of information using web search
        """
        return tavily_search.func(
            query=f"fact check: {claim}",
            max_results=3
        ) 