import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    VAPI_API_KEY = os.getenv('VAPI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # CRM Settings
    CRM_SPREADSHEET_PATH = os.getenv('CRM_SPREADSHEET_PATH') #MODIFY
    
    # Ticketing System Settings
    # TICKET_SYSTEM_API_URL = os.getenv('TICKET_SYSTEM_API_URL')
    # TICKET_SYSTEM_API_KEY = os.getenv('TICKET_SYSTEM_API_KEY')

    # ^ Simply put a column in the spreadsheet with the name of the ticketing system and the ticket number

    # Call Settings
    MAX_CALL_DURATION = 300  # 5 minutes
    SILENCE_TIMEOUT = 30     # 30 seconds of silence before ending call