from browser_use import Agent, Browser, BrowserConfig, Controller, ActionResult
from tools.tavily_search import TavilySearchTool
from typing import Dict, List

# Initialize the controller
controller = Controller()

@controller.action('Before buying anything, ask the user for confirmation')
def ask_human(question: str) -> str:
    confirmation = input(f'\n⚠️ This appears to be a purchase. Are you sure you want to proceed with "{question}"? (yes/no): ')
        
    # Only proceed if user explicitly confirms
    if confirmation.lower() not in ['yes', 'y']:
        return ActionResult(extracted_content='Purchase cancelled by user')

    return ActionResult(extracted_content='Purchase confirmed by user')


class WebSearchAgent:
    def __init__(self, llm):
        """
        Initialize the WebSearchAgent with both Tavily and Browser Use capabilities.
        
        Args:
            llm: Language model instance for Browser Use
        """
        self.llm = llm
        self.tavily_tool = TavilySearchTool()

    def get_agent(self):
        return self

    def _create_browser_instruction(self, url: str, query: str) -> str:
        """
        Create a clear browser instruction based on the query type.
        """
        # Extract action keywords to determine instruction type
        query_lower = query.lower()
        
        # Create a prompt to extract the intended action from the query
        action_prompt = [{"role": "user", "content": f"""
            From this user query: "{query}"
            Extract the main action verb that describes what needs to be done.
            Return ONLY the verb in present tense (e.g. 'find', 'purchase', 'download', etc).
            Do not include any other words or punctuation.
        """}]
        
        try:
            # Get the action from the language model
            action_response = self.llm.run(action_prompt)
            action = action_response.content.strip().lower()
            
            # Create a custom instruction using the model-determined action
            target = query_lower.replace(action, '').strip()
            return f"Go to {url} and {action} {target}"
        except Exception as e:
            # Fallback to basic instruction if action extraction fails
            return f"Go to {url} and find information about {query}"

    async def run(self, task: Dict) -> str:
        """
        Execute search flow: Tavily for URLs -> Browser Use for actions
        """
        query = task.get("task", "").strip()
        if not query:
            return "No search query provided."
        
        if "amazon" in query.lower():
            print("Amazon detected, using Brave Browser")
            browser = Browser(
                    config=BrowserConfig(
                        # Specify the path to your Chrome executable
                        chrome_instance_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
                    )
                )
                
            browser_agent = Agent(
                task=f"Go to https://www.amazon.es/ and {query}",
                llm=self.llm,
                browser=browser,
                controller=controller
            )

            result = await browser_agent.run()

            return result
                


        # Get relevant URLs using Tavily
        print("\n🔍 Finding relevant URLs with Tavily...")
        relevant_urls = self.tavily_tool.get_relevant_urls(query)
        
        if not relevant_urls:
            return "No relevant URLs found for the query."

        # Print found URLs
        print("\n📚 Found the following relevant sources:")
        for idx, url in enumerate(relevant_urls, 1):
            print(f"{idx}. {url}")

        print("\n🤖 Processing URLs with Browser Use...")
        
        # Process URLs one by one until task is completed
        for idx, url in enumerate(relevant_urls, 1):
            try:
                print(f"\n🌐 Trying URL {idx}/{len(relevant_urls)}: {url}")
                browser_instruction = self._create_browser_instruction(url, query)
                print(f"📝 Instruction: {browser_instruction}")

                # browser = Browser(
                #     config=BrowserConfig(
                #         # Specify the path to your Chrome executable
                #         chrome_instance_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',  # macOS path
                #         # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                #         # For Linux, typically: '/usr/bin/google-chrome'
                #     )
                # )
                
                browser_agent = Agent(
                    task=browser_instruction,
                    llm=self.llm,
                    # browser=browser
                )
                
                result = await browser_agent.run()
                
                if "not found" not in result.lower() and "error" not in result.lower():
                    return f"✅ Task completed successfully at {url}:\n{result}"
                
                print("⚠️  Could not complete task with this URL, trying next...")
                continue
                
            except Exception as e:
                print(f"❌ Error with URL {idx}: {str(e)}")
                continue
        
        return "❌ Could not complete the task with any of the provided URLs."