import asyncio
from agents.search_agent import WebSearchAgent
from langchain_openai import ChatOpenAI
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class WebAssistant:
    """
    Web Assistant that combines planning and intelligent web search capabilities
    using Tavily for URL discovery and Browser Use for detailed web interaction.
    """
    def __init__(self):
        # Initialize language model for agents
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",  
            temperature=0.3
        )
        
        # Initialize the search agent
        self.search_agent = WebSearchAgent(
            llm=self.llm
        ).get_agent()
    
    async def handle_query(self, user_input: str) -> str:
        """
        Direct flow: User Query -> Tavily Search -> Browser Use Action
        """
        try:
            search_task = {"task": user_input}
            result = await self.search_agent.run(search_task)
            return result
            
        except Exception as e:
            return f"An error occurred: {str(e)}"

async def main():
    """
    Main function to run the Web Assistant interface.
    """
    assistant = WebAssistant()
    
    print("🌐 Welcome to Web Assistant!")
    print("Type your query or 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\n❓ ¿Qué quieres que haga? > ")
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Gracias por usar Web Assistant. Adiós!")
                break
            
            print("\n🔄 Procesando...")
            result = await assistant.handle_query(user_input)
            
            # Display results
            print("\n📝 Resultados:")
            print(result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    asyncio.run(main()) 