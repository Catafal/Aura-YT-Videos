# python3 -m venv venv (para crear un entorno virtual)
# source venv/bin/activate (para activar el entorno virtual)
# pip install crewai tools (para instalar las dependencias)
# python reddit.py (para ejecutar el script)

from crewai import Crew, Process

from agents import RedditAgents
from tasks import RedditTasks
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OpenAIGPT4 = OpenAI(model="gpt-4o-mini") #api_key=os.getenv("OPENAI_API_KEY")

agents = RedditAgents()
tasks = RedditTasks()



things_to_promote = """
Canal de YouTube sobre IA (https://www.youtube.com/channel/UCrXSVX9a1mj810CMLwkGvMw), a continuación los 3 videos más recientes:
1. Cómo construir un agente de ventas con IA que puede contactar prospectos, realizar llamadas en frío y hacer seguimiento por WhatsApp.
2. Cómo reducir los costos de Modelos de Lenguaje Grande para tus aplicaciones de IA (Al desarrollar aplicaciones de IA, la optimización del modelo LLM es importante).
3. Cómo construir un web scraper universal para extraer datos de sitios web con Agentes de IA.
"""

# Configuración de agentes
reddit_post_finder = agents.reddit_post_finder()
reddit_comment_writer = agents.reddit_comment_writer()
reddit_comment_poster = agents.reddit_comment_poster()

# Configuración de tareas
search_recent_reddit_post_task = tasks.search_recent_reddit_post_task(
    reddit_post_finder, things_to_promote
)

draft_reddit_comment = tasks.draft_reddit_comment(
    reddit_comment_writer, [search_recent_reddit_post_task]
)

post_reddit_comment = tasks.post_reddit_comment(
    reddit_comment_poster, [draft_reddit_comment]
)

# Configuración de herramientas
crew = Crew(
    agents=[reddit_post_finder, reddit_comment_writer, reddit_comment_poster],
    tasks=[search_recent_reddit_post_task, draft_reddit_comment, post_reddit_comment],
    process=Process.hierarchical,
    manager_llm=OpenAIGPT4,
)

results = crew.kickoff()

print(results)