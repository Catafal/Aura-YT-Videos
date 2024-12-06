import praw
from crewai.tools import tool
from dotenv import load_dotenv
import os
from typing import Dict, Any

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
)

class RedditTools:
    @staticmethod
    @tool("Buscar publicaciones recientes de reddit")
    def search_recent_reddit_post(keywords: str) -> Dict[str, Any]:
        """Buscar publicaciones recientes de reddit basadas en palabras clave"""
        try:
            subreddit = reddit.subreddit("all")
            posts = []
            for submission in subreddit.search(
                keywords, time_filter="hour", sort="new", limit=5
            ):
                if not submission.locked and submission.is_self and not submission.archived:
                    post = {
                        "title": submission.title,
                        "content": submission.selftext,
                        "url": submission.url,
                        "submission_id": submission.id,
                    }
                    posts.append(post)
            return {"posts": posts}  # Return as a dictionary
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    @tool("Obtener contenido de publicación de reddit")
    def fetch_reddit_post_content(submission_id: str) -> Dict[str, str]:
        """Obtener el contenido de una publicación de Reddit dado su ID"""
        try:
            submission = reddit.submission(id=submission_id)
            content = submission.selftext if submission.is_self else f"Link post content: {submission.url}"
            return {
                "content": content,
                "title": submission.title,
                "url": submission.url
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    @tool("Comentar en publicación de reddit")
    def reply_to_reddit_post(submission_id: str, message: str) -> Dict[str, str]:
        """Publicar comentario en publicación de Reddit"""
        try:
            submission = reddit.submission(id=submission_id)
            comment = submission.reply(message)
            return {
                "status": "success",
                "url": f"https://www.reddit.com{comment.permalink}",
                "comment_id": comment.id
            }
        except Exception as e:
            return {"error": str(e)}