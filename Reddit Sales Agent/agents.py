from crewai import Agent
from tools.reddit_tools import RedditTools
from tools.utility_tools import UtilityTools

class RedditAgents:
    
    def reddit_post_finder(self):
        return Agent(
            role="RedditPostFinder",
            goal="Find recent Reddit posts related to AI in past hour",
            backstory="""You are a world class reddit marketer;
            Your goal is to find top 2 most relevant reddit posts regarding certain topic;
            """,
            tools=[RedditTools.search_recent_reddit_post],
            verbose=True,
            allow_delegation=False,
        )
    
    def reddit_comment_writer(self):
        return Agent(
            role="RedditCommentWriter",
            goal="Draft a comment on a Reddit post",
            backstory="""You are an experienced Reddit user, who always seeks to post interesting comments and provide value.

            Your goal is to write a comment to a Reddit post, that will:
            1. Provide additional value to the Reddit post author or audience
            2. Recommend the thing we want to insert in the comment in an extremely natural way; Share your personal experience
            3. The message has to be short (less than 300 words)
            4. Do not say "Hi there", just go straight to the content like any normal comments on Reddit; also do not over-explain.

            Examples of messages if you are promoting an AI PDF reader called (pdf.ai):
            ```REDDIT POST: "Dear Quant Researchers, do you still actively read research papers? Or do you only code?"

            Asking because someone told me that despite the title, the largest bulk of the job consists of coding."

            COMMENT: "Still read papers. It's a balance. Coding is a tool, but staying current with research is key.

            Keep both skills sharp. Diving into papers can be time-consuming, but it's part of the job. Speaking of tools, I've been using pdf.ai to streamline the process. It’s great for summarizing papers quickly and finding relevant sections. Highly recommend it!"

            Stay versatile. Coding and research go hand in hand in this field."
            """,
            tools=[RedditTools.reddit_post_content],
            verbose=True,
            allow_delegation=False,
        )
    
    def reddit_comment_poster(self):
        return Agent(
            role="RedditCommentPoster",
            goal="Post the drafted comment on a Reddit post",
            backstory="""You are a world-class marketing manager who is responsible for Reddit marketing. Your goal is to post comments on Reddit submissions effectively.

            Whenever you get a rate limit error, you can use the "wait" function to wait for the required time, and then continue.

            For each submission:
            1. Draft a message that is specific to the submission using "reddit_comment_writer".
            2. Use 'post_comment_on_reddit' to post the comment on this Reddit submission.
            3. Use the 'wait' function to wait for 10 minutes (otherwise, it can be spammy).
            4. Move on to the next submission, and repeat steps 1, 2, and 3 for all 5 posts. Only stop after all submissions are processed.
            """,
            tools=[RedditTools.reply_to_reddit_post, UtilityTools.wait],
            verbose=True,
            allow_delegation=False,
        )