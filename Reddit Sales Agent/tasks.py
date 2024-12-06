from datetime import datetime
from crewai import Task

class RedditTasks:
    def search_recent_reddit_post_task(self, agent, things_to_promote):
        return Task(
            description=f"""COSAS QUE QUEREMOS PROMOVER Y PROMOCIONAR:
            {things_to_promote}

            OBJETIVO:
            Encuentra 2 publicaciones relevantes de Reddit donde podamos aportar valor y promocionar las cosas que queremos promover.
            Si no encuentras publicaciones relevantes, simplemente devuelve 'no hay publicaciones relevantes en la última hora'.

            El resultado devuelto debe ser 2 publicaciones de Reddit más relevantes, incluyendo título, URL, submission_id y razón.
            Ejemplo de Salida: 'título': 'La IA toma protagonismo en los anuncios del Super Bowl', 'url': 'https://reddit.com/...'
            """,
            agent=agent,
            expected_output = """
                Una lista de las 2 publicaciones más relevantes de Reddit sobre un tema determinado.
                Ejemplo de Salida:
                [
                    {
                        'título': 'La IA toma protagonismo en los anuncios del Super Bowl',
                        'url': 'https://reddit.com/post1',
                        'submission_id': '1bd3tac',
                        'razonamiento': 'Esta publicación es relevante porque discute el uso de la IA en la publicidad.'
                    },
                    ...
                ]
            """,
        )

    def draft_reddit_comment(self, agent, context):
        return Task(
            description="Redactar un comentario en una publicación de Reddit basado en el título, submission_id de las publicaciones y razonamiento",
            agent=agent,
            context=context,
            expected_output = "Un comentario redactado en la publicación, así como un submission_id",
        )
    
    def post_reddit_comment(self, agent, context):
        return Task(
            description="Publicar el comentario generado desde draft_reddit_comment en la publicación de Reddit basado en el submission_id",
            agent=agent,
            context=context,
            expected_output = "La URL del comentario que fue publicado en la publicación de Reddit",
        )