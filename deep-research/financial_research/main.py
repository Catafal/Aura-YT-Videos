from crewai import Crew, Agent, Task
from agents.writer import create_writer_agent
from financial_research.agents.researcher import ResearchAgent
from financial_research.agents.analyst import AnalystAgent
from langchain_ollama import OllamaLLM

def create_financial_research_crew(research_topic: str):
    """
    Creates and configures the financial research crew with all necessary agents.
    
    Args:
        research_topic: The specific topic or market to research
    """
    # Initialize agents
    researcher = ResearchAgent.create()
    analyst = AnalystAgent.create()
    writer = create_writer_agent()
    
    # Define tasks
    research_task = Task(
        description=f"Research comprehensive market information about {research_topic}. "
                   f"Use available scraping tools to gather data from reliable sources.",
        expected_output="A detailed report on the market research topic",
        agent=researcher
    )
    
    analysis_task = Task(
        description=f"Analyze the gathered market data for {research_topic}. "
                   f"Identify key trends, opportunities, and risks.",
        expected_output="A detailed analysis of the market research topic",
        agent=analyst
    )
    
    writing_task = Task(
        description=f"Create a detailed markdown report about {research_topic} "
                   f"based on the research and analysis provided.",
        expected_output="A detailed markdown report on the market research topic",
        agent=writer
    )
    
    # Create crew
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        output_log_file="financial_research_output.log"
    )
    
    return crew

def analyze_company(company_name: str):
    """
    Perform comprehensive company analysis using a crew of agents
    
    Args:
        company_name: Name of the company to analyze
    """
    # Create agents
    researcher = ResearchAgent.create()
    analyst = AnalystAgent.create()
    writer = create_writer_agent()
    
    # Define tasks
    research_task = Task(
        description=f"""Research {company_name} thoroughly. Find:
            1. Latest financial reports
            2. News and press releases
            3. Market position and competitors
            4. Key financial metrics""",
        expected_output="A comprehensive research report with financial data, news, and market information",
        agent=researcher
    )
    
    analysis_task = Task(
        description=f"""Analyze all gathered information about {company_name} and provide:
            1. Financial health assessment
            2. Growth prospects
            3. Risk factors
            4. Investment recommendation""",
        expected_output="A detailed analysis report with financial assessment and recommendations",
        agent=analyst
    )
    
    writing_task = Task(
        description=f"""Create a detailed markdown report about {company_name} that includes:
            1. Company Overview
            2. Financial Analysis
            3. Market Position
            4. Risk Assessment
            5. Investment Recommendation
            
            Use the research and analysis provided by other agents.
            Format the report professionally with clear sections and bullet points.""",
        expected_output="A well-formatted markdown report with comprehensive company analysis",
        agent=writer
    )
    
    # Create and run the crew
    crew = Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task]
    )
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    print("Choose analysis type:")
    print("1. Market Research")
    print("2. Company Analysis")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    while choice not in ['1', '2']:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == '1':
        topic = input("Enter the market research topic (e.g. 'AI market trends 2024'): ").strip()
        while not topic:
            print("Topic cannot be empty. Please try again.")
            topic = input("Enter the market research topic: ").strip()
        crew = create_financial_research_crew(topic)
        result = crew.kickoff()
    else:
        company = input("Enter company name to analyze (e.g. 'Tesla'): ").strip()
        while not company:
            print("Company name cannot be empty. Please try again.")
            company = input("Enter company name to analyze: ").strip()
        result = analyze_company(company)
    
    print("\nAnalysis Result:")
    print(result)
