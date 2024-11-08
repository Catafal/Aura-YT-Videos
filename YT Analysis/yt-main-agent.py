# pip install openai python-dotenv agentql playwright && agentql init(para instalar las dependencias)
# python yt-main-agent.py (para ejecutar el script)

import os
from openai import OpenAI
from dotenv import load_dotenv
import agentql
from playwright.sync_api import sync_playwright

# Initialize API client
load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY")
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def get_channel_info(channel_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = agentql.wrap(browser.new_page())
        page.goto(channel_url)
        
        # AgentQL query to get channel stats
        CHANNEL_QUERY = """
        {
            channel_name
            subscriber_count
            total_videos
            recent_videos[] {
                title
                views
                published_date
            }
        }
        """
        
        data = page.query_data(CHANNEL_QUERY)
        browser.close()
        return data

def get_youtube_analysis(channel_data):
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": """You are an AI specialist in YouTube channel analysis. 
            Your task is to analyze channel data and create insightful reports focused on content strategy, 
            audience engagement, and publishing patterns. Pay special attention to what makes videos succeed or underperform."""},
            {"role": "user", "content": f"""Please analyze this YouTube channel data and create a markdown report 
            that includes:

            1. Channel Overview
            2. Top 3 Performing Videos
               - List the videos with their views
               - Analyze titles for patterns
               - What likely made these videos successful?
            
            3. Bottom 3 Performing Videos
               - List the videos with their views
               - Analyze potential reasons for lower performance
               - Suggestions for improvement
            
            4. Engagement Analysis
               - Suggestions to improve audience engagement
               - Identify common engagement patterns
            
            5. Content Analysis
               - Identify top-performing content themes
               - Suggest future content ideas
               - Analyze audience engagement
            
            6. Publishing Patterns
               - Best days and times to publish
               - Frequency of publishing
            
            7. Title optimization recommendations
               - Analyze top-performing titles
               - Suggest improvements
            
            8. Growth Opportunities & Recommendations
               - Identify potential growth areas
               - Suggest strategies to increase viewership
            
            Here's the data:
            {channel_data}"""}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    return completion.choices[0].message.content

# Example usage
if __name__ == "__main__":
    # Create analyses directory if it doesn't exist
    analyses_dir = "youtube_analyses"
    if not os.path.exists(analyses_dir):
        os.makedirs(analyses_dir)

    channel_url = "https://www.youtube.com/@AlexHormozi/videos"
    channel_data = get_channel_info(channel_url)
    channel_name = channel_data["channel_name"]
    
    # Print truncated data
    print("\nChannel Information (preview):")
    print(str(channel_data)[:100] + "...")
    
    # Get analysis from Grok
    analysis = get_youtube_analysis(channel_data)
    
    # Save to markdown file in the analyses directory
    output_path = os.path.join(analyses_dir, f"youtube_analysis_{channel_name}.md")
    with open(output_path, "w") as f:
        f.write(analysis)
    
    print(f"\nAnalysis has been saved to {output_path}")
