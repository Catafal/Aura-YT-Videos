# python3 -m venv venv (para crear un entorno virtual)
# source venv/bin/activate (para activar el entorno virtual)
# pip install crewai tools (para instalar las dependencias)
# python reddit.py (para ejecutar el script)

from crewai import Crew, Process

from agents import RedditAgents
from tasks import RedditTasks
from langchain.openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OpenAIGPT4 = ChatOpenAI(model="gpt-4")

agents = RedditAgents()
tasks = RedditTasks()

things_to_promote = """
AI YouTube channel (https://www.youtube.com/channel/UCrXSVX9a1mj810CMLwkGvMw), below are 3 of the most recent videos:
1. How to build an AI sales agent that can outreach prospects, cold call them, and follow up on WhatsApp.
2. How to reduce Large Language Model costs for your AI applications (When developing AI applications, LLM model optimization matters).
3. How to build a universal web scraper to scrape websites with AI Agents.
"""

# Setting up agents
reddit_post_finder = agents.reddit_post_finder()
reddit_comment_writer = agents.reddit_comment_writer()
reddit_comment_poster = agents.reddit_comment_poster()

# Setting up tasks
search_recent_reddit_post_task = tasks.search_recent_reddit_post_task(
    reddit_post_finder, things_to_promote
)

draft_reddit_comment = tasks.draft_reddit_comment(
    reddit_comment_writer, [search_recent_reddit_post_task]
)

post_reddit_comment = tasks.post_reddit_comment(
    reddit_comment_poster, [draft_reddit_comment]
)

# Setting up tools
crew = Crew(
    agents=[reddit_post_finder, reddit_comment_writer, reddit_comment_poster],
    tasks=[search_recent_reddit_post_task, draft_reddit_comment, post_reddit_comment],
    process=Process.hierarchical,
    manager_llm=OpenAIGPT4,
)

results = crew.kickoff()

print(results)