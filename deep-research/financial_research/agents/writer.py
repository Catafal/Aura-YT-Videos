from crewai import Agent, LLM
from langchain_openai import OpenAI
from langchain_ollama import ChatOllama

def create_writer_agent() -> Agent:
    """
    Creates a writer agent specialized in creating clear, well-structured
    financial reports in markdown format.
    """
    return Agent(
        role='Financial Report Writer',
        goal='Create comprehensive, well-structured market reports in markdown format',
        backstory="""You are an experienced financial writer who excels at 
                    creating clear, concise, and informative reports. You have 
                    a talent for presenting complex information in an 
                    accessible format.""",
        tools=[],  # Writer primarily uses cognitive abilities
        verbose=True,
        # llm=OpenAI(model="gpt-4o-mini")
        llm= LLM(model="ollama/deepseek-r1:14b", base_url="http://localhost:11434")
    ) 