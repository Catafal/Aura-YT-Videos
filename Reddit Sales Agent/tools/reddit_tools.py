import praw
from langchain.tools import tool
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Now you can access the environment variables as before
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password,
)

class RedditTools:
    @tool("Search for recent reddit posts")
    def search_recent_reddit_post(keywords):
        """Search recent reddit posts based on keywords"""

        # Choose the subreddit you want to search in
        subreddit = reddit.subreddit("all")  # 'all' searches across all of Reddit

        # Search for submissions related to certain keywords within the last day
        keywords = keywords
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
        
        return posts
    
    @tool("Fetch reddit post content")
    def fetch_reddit_post_content(submission_id):
        """Fetch the content of a Reddit post"""
        submission = reddit.submission(id=submission_id)
        
        if submission.is_self:
            return f"Content: {submission.selftext}"
        else:
            return f"This is a link post, Content: {submission.selftext}"

    @tool("Post comment on reddit post")
    def reply_to_reddit_post(submission_id, message):
        """Post comment on Reddit post"""
        submission = reddit.submission(id=submission_id)
        comment = submission.reply(message)
        comment_url = f"https://www.reddit.com{comment.permalink}"
        
        return f"Successfully left comment, here is the link: {comment_url}"