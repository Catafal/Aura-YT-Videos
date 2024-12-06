from crewai import Agent
from tools.reddit_tools import RedditTools
from tools.utility_tools import UtilityTools

class RedditAgents:
    
    def reddit_post_finder(self):
        return Agent(
            role="RedditPostFinder",
            goal="Encontrar publicaciones recientes de Reddit relacionadas con IA en la última hora",
            backstory="""Eres un experto en marketing de Reddit de clase mundial;
            Tu objetivo es encontrar las 2 publicaciones más relevantes de Reddit sobre cierto tema;
            """,
            tools=[RedditTools.search_recent_reddit_post],
            verbose=True,
            allow_delegation=False,
        )
    
    def reddit_comment_writer(self):
        return Agent(
            role="RedditCommentWriter",
            goal="Redactar un comentario en una publicación de Reddit",
            backstory="""Eres un usuario experimentado de Reddit que siempre busca publicar comentarios interesantes y aportar valor.
            
            Tu objetivo es escribir un comentario en una publicación de Reddit que:
            1. Proporcione valor adicional al autor o audiencia de la publicación.
            2. Recomiende lo que queremos insertar en el comentario de una manera extremadamente natural; comparte tu experiencia personal.
            3. El mensaje debe ser corto (menos de 300 palabras).
            4. No digas "Hola", ve directo al contenido como cualquier comentario normal en Reddit; tampoco sobreexplique.
            
            Ejemplos de mensajes si estás promocionando un lector de PDF con IA llamado (pdf.ai):
            [Ejemplo de mensaje]
            """,
            tools=[RedditTools.fetch_reddit_post_content],
            verbose=True,
            allow_delegation=False,
        )
    
    def reddit_comment_poster(self):
        reddit_tools = RedditTools()
        utility_tools = UtilityTools()
        
        return Agent(
            role="RedditCommentPoster",
            goal="Publicar el comentario redactado en una publicación de Reddit",
            backstory="""Eres un gerente de marketing de clase mundial responsable del marketing en Reddit. Tu objetivo es publicar comentarios en las publicaciones de Reddit de manera efectiva.
            
            Cuando recibas un error de límite de tasa, puedes usar la función "wait" para esperar el tiempo requerido y luego continuar.
            
            Para cada publicación:
            1. Redacta un mensaje específico para la publicación usando "reddit_comment_writer".
            2. Usa 'reply_to_reddit_post' para publicar el comentario en esta publicación.
            3. Usa la función 'wait' para esperar 10 minutos (de lo contrario, puede ser spam).
            4. Pasa a la siguiente publicación y repite los pasos 1, 2 y 3 hasta procesar todas las publicaciones.
            """,
            tools=[reddit_tools.reply_to_reddit_post, utility_tools.wait],
            verbose=True,
            allow_delegation=False,
        )


    