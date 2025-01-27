from typing import List, Optional
import json
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage

from configuration import Configuration
from utils import deduplicate_and_format_sources, tavily_search, format_sources
from prompts import (
    query_writer_instructions,
    summarizer_instructions,
    reflection_instructions,
    local_answer_system_prompt,
    local_answer_context_prompt,
    enhanced_summarizer_instructions
)

class ConsoleResearcher:
    """Console-based research assistant that performs iterative web research."""
    
    def __init__(self, config: Optional[Configuration] = None):
        """Initialize the researcher with configuration."""
        self.config = config or Configuration()
        self.llm = ChatOllama(model=self.config.local_llm, temperature=0)
        self.llm_json = ChatOllama(model=self.config.local_llm, temperature=0, format="json")
        self.memory = ConversationBufferMemory()
        
    def answer_question(self, question: str) -> str:
        """First try to answer with local LLM, then fall back to web research if needed."""
        print("\nAnalyzing your question with local LLM...\n")
        
        # Get conversation history
        history = self._get_conversation_history()
        
        # First, try to answer with local LLM
        initial_response = self._get_local_answer(question, history)
        
        # Store the interaction in memory
        self.memory.save_context(
            {"input": question},
            {"output": initial_response}
        )
        
        # Check if the model admits to uncertainty
        if self._needs_web_search(initial_response):
            print("\nNeed to search the web for more accurate information...")
            web_response = self.research(question)
            # Store the web research response in memory
            self.memory.save_context(
                {"input": "Web research results for: " + question},
                {"output": web_response}
            )
            return web_response
        else:
            print("\nFound answer from local knowledge.")
            return initial_response
        
    def _get_local_answer(self, question: str, history: str) -> str:
        """Get answer from local LLM using conversation history."""
        context_prompt = local_answer_context_prompt.format(
            history=history,
            question=question
        )
        
        result = self.llm.invoke([
            SystemMessage(content=local_answer_system_prompt),
            HumanMessage(content=context_prompt)
        ])
        return result.content
        
    def _get_conversation_history(self) -> str:
        """Get formatted conversation history from memory."""
        history = self.memory.load_memory_variables({})
        if "history" in history and history["history"]:
            return history["history"]
        return "No previous conversation."
        
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
        
    def _needs_web_search(self, response: str) -> bool:
        """Check if the response indicates need for web search."""
        uncertainty_indicators = [
            "need to search",
            "not sure",
            "cannot provide",
            "don't have",
            "would need to verify",
            "uncertain",
            "I apologize",
            "I don't know"
        ]
        return any(indicator.lower() in response.lower() for indicator in uncertainty_indicators)

    def research(self, topic: str) -> str:
        """Perform iterative research on a topic."""
        print(f"\nStarting research on: {topic}\n")
        
        research_loop_count = 0
        running_summary = None
        sources_gathered = []
        
        while research_loop_count < self.config.max_web_research_loops:
            # Generate search query
            print("Generating search query...")
            print("=" * 80)
            query = self._generate_query(topic)
            print(f"Search query: {query}\n")
            
            # Perform web research
            print("Searching the web...")
            search_results = tavily_search(query, include_raw_content=True, max_results=1)
            search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000)
            sources_gathered.append(format_sources(search_results))
            print("Found new sources\n")
            
            # Summarize findings
            print("Summarizing information...")
            running_summary = self._summarize_sources(topic, search_str, running_summary)
            print(f"\nCurrent summary:\n{running_summary}\n")
            
            # Reflect and decide on follow-up
            if research_loop_count < self.config.max_web_research_loops - 1:
                print("Reflecting on findings...")
                follow_up = self._reflect_on_summary(topic, running_summary)
                print(f"Identified knowledge gap: {follow_up}\n")
            
            research_loop_count += 1
            
        # Finalize summary with sources
        all_sources = "\n".join(sources_gathered)
        final_summary = f"## Summary\n\n{running_summary}\n\n### Sources:\n{all_sources}"
        return final_summary
    
    def _generate_query(self, topic: str) -> str:
        """Generate a search query for the topic."""
        result = self.llm_json.invoke([
            SystemMessage(content=query_writer_instructions),
            HumanMessage(content=f"Generate a detailed search query for: {topic}")
        ])
        return json.loads(result.content)['query']
    
    def _summarize_sources(self, topic: str, new_research: str, existing_summary: Optional[str]) -> str:
        """Summarize research results."""
        if existing_summary:
            prompt = (
                f"Using the detailed instructions below, extend the existing summary with new information:\n\n"
                f"Existing Summary:\n{existing_summary}\n\n"
                f"New Research to Integrate:\n{new_research}\n\n"
                f"Topic: {topic}"
            )
        else:
            prompt = (
                f"Using the detailed instructions below, create a comprehensive summary of:\n\n"
                f"Research Results:\n{new_research}\n\n"
                f"Topic: {topic}"
            )
            
        result = self.llm.invoke([
            SystemMessage(content=enhanced_summarizer_instructions),
            HumanMessage(content=prompt)
        ])
        
        summary = result.content
        
        # Remove thinking tags if present
        while "<think>" in summary and "</think>" in summary:
            start = summary.find("<think>")
            end = summary.find("</think>") + len("</think>")
            summary = summary[:start] + summary[end:]
            
        return summary
    
    def _reflect_on_summary(self, topic: str, summary: str) -> str:
        """Reflect on the current summary and identify knowledge gaps."""
        reflection_prompt = reflection_instructions.format(research_topic=topic)
        result = self.llm_json.invoke([
            SystemMessage(content=reflection_prompt),
            HumanMessage(content=f"Identify a knowledge gap and generate a follow-up web search query based on our existing knowledge: {summary}")
        ])
        return json.loads(result.content)['follow_up_query']

def print_help():
    """Print help information about available commands."""
    help_text = """
Available Commands:
==================
help        - Show this help message
clear memory - Clear the conversation history and start fresh
quit        - Exit the program

Tips:
-----
- Ask any question and I'll try to answer using my knowledge
- If I'm unsure, I'll automatically search the web for accurate information
- I remember our conversation to provide more contextual answers
- Use 'clear memory' if you want to start a new topic from scratch
"""
    print(help_text)

def main():
    """Main entry point for the console researcher."""
    researcher = ConsoleResearcher()
    
    print("Welcome to the Research Assistant!")
    print("I'll try to answer from my knowledge first, and search the web if needed.")
    print("Type 'help' for available commands.")
    
    while True:
        question = input("\nWhat would you like to know? ").strip()
        
        if question.lower() == 'quit':
            print("\nGoodbye!")
            break
        elif question.lower() == 'clear memory':
            researcher.clear_memory()
            print("\nMemory cleared. Starting fresh conversation.")
            continue
        elif question.lower() == 'help':
            print_help()
            continue
            
        try:
            answer = researcher.answer_question(question)
            print("\nAnswer:")
            print("=" * 80)
            print(answer)
            print("=" * 80)
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main() 