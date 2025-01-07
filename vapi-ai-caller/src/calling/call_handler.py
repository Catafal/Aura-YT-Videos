from vapi_python import Vapi
from typing import Dict, Optional
import time
from datetime import datetime


class CallHandler:
    def __init__(self, api_key: str):
        """Initialize the VAPI client with authentication.
        
        The CallHandler uses VAPI's official Python SDK to manage calls.
        It maintains a reference to the active call to enable operations
        like stopping and status checking.
        
        Args:
            api_key (str): Your VAPI API key for authentication
        """
        self.vapi = Vapi(api_key=api_key)
        self.active_call = None
        self.call_start_time = None

    def make_call(self, phone_number: str) -> Dict:
        """Initiate an outbound call using VAPI's AI assistant.
        
        This method configures an AI assistant to handle the call,
        including setting up the conversation context and parameters
        for natural interaction.
        
        Args:
            phone_number (str): The customer's phone number to call
            
        Returns:
            Dict: Call information including status and call ID
        """
        # Configure the AI assistant for customer service
        assistant = {
            'firstMessage': "Hola! Aquí Diego de Aura Systems. ¿en qué puedo ayudarte?",
            'context': """You are a professional customer service representative making a follow-up call.
                      Your goal is to:
                      1. Confirm it's a good time to talk
                      2. Get feedback on their experience
                      3. Identify any issues or concerns
                      4. Document any action items
                      Be polite, professional, and respect the customer's time.""",
            'model': 'llama-3.1-70b-versatile',  # Using GPT-4 for better comprehension
            'voice': 'jennifer-playht',  # Using a natural-sounding voice
            'recordingEnabled': True,  # Enable recording for transcription
            'interruptionsEnabled': True,  # Allow natural back-and-forth
            'endCallTriggers': [  # Conditions to end the call gracefully
                "goodbye",
                "thank you for your time",
                "have a great day"
            ]
        }
        
        # Set up variable values that might be needed during the call
        assistant_overrides = {
            'variableValues': {
                'phone_number': phone_number,
                'call_time': datetime.now().strftime("%I:%M %p")
            }
        }

        try:
            # Start the call using the VAPI SDK
            self.active_call = self.vapi.start(
                assistant=assistant,
                assistant_overrides=assistant_overrides
            )
            # self.active_call = self.vapi.start(
            #     assistant="ceea1ffd-52bd-448a-abf5-6afdd33d7d8e",
            #     assistant_overrides=assistant_overrides
            # )
            self.call_start_time = datetime.now()
            
            return {
                'call_id': self.active_call.id,
                'status': 'initiated',
                'start_time': self.call_start_time
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to initiate call: {str(e)}")

    def stop_call(self) -> None:
        """Stop the currently active call.
        
        This method gracefully ends the ongoing call if one exists.
        It's important to call this to properly close the connection
        and ensure all call data is saved.
        """
        if self.active_call:
            try:
                self.vapi.stop()
                self.active_call = None
                self.call_start_time = None
            except Exception as e:
                raise RuntimeError(f"Failed to stop call: {str(e)}")

    def get_call_details(self, call_id: str, max_wait_seconds: int = 300) -> Dict:
        """Retrieve the details and transcript of a completed call.
        
        This method waits for the call to complete and then returns
        comprehensive information about the call, including the
        transcript and any AI-generated insights.
        
        Args:
            call_id (str): The ID of the call to retrieve
            max_wait_seconds (int): Maximum time to wait for call completion
            
        Returns:
            Dict: Complete call details including transcript and status
        """
        start_time = time.time()
        call_completed = False
        
        while time.time() - start_time < max_wait_seconds:
            try:
                # Get current call status
                call_info = self.vapi.get_call(call_id)
                
                # Check if call is complete
                if call_info.get('status') in ['completed', 'failed', 'ended']:
                    call_completed = True
                    break
                
                # Wait before checking again
                time.sleep(10)
                
            except Exception as e:
                raise RuntimeError(f"Failed to get call details: {str(e)}")
        
        if not call_completed:
            raise TimeoutError("Call did not complete within the specified time")
        
        # Return comprehensive call information
        return {
            'call_id': call_id,
            'status': call_info.get('status'),
            'duration': call_info.get('duration'),
            'transcript': call_info.get('transcript'),
            'summary': call_info.get('summary'),
            'sentiment': call_info.get('sentiment'),
            'action_items': call_info.get('action_items'),
            'end_time': datetime.now()
        }

    def __del__(self):
        """Cleanup method to ensure we don't leave any active calls.
        
        This destructor ensures that any ongoing calls are properly
        terminated when the CallHandler object is destroyed.
        """
        if self.active_call:
            try:
                self.stop_call()
            except:
                pass  # Ignore cleanup errors