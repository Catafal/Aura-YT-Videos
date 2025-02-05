# GOAL
- create a researcher capable of scraping a website and extracting information
- the researcher should be able to use LLM to understand the information
- the researcher should be able to save the information in markdown format

- we are going to use LangChain and CrewAI to create the researcher
- Also we are going to have 2 models in place, o3-mini and deepseek-r1:14b (private and open source)

- we are going to use Serper, Firecrawl, Spider, Tavily, apify

- The agent is going to specialize in analysing markets, and then create a report with the information found.

- Multi agent environment, where we have the following agents:
    - researcher
    - financial analyst
    - writer
    - investment advisor
    - quant analyst

https://docs.crewai.com/introduction

    
