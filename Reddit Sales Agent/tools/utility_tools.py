import time
from langchain.tools import tool

class UtilityTools:
    @tool("Wait for certain amount of time")
    def wait(mins):
        """Wait for a certain amount of time"""
        duration_in_seconds = mins * 60
        time.sleep(duration_in_seconds)
        
        print(f"Great, you've waited {mins} mins! Now proceed with your task.")
        return f"Great, you've waited {mins} mins! Now proceed with your task."