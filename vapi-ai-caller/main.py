import time
from typing import Optional
from src.crm.spreadsheet_manager import SpreadsheetManager
from src.calling.call_handler import CallHandler
from src.summarization.call_summarizer import CallSummarizer
from config.config import Config

class CRMCaller:
    def __init__(self):
        """Initialize the CRM Caller with all necessary components."""
        print("Initializing CRM Caller system...")
        self.crm = SpreadsheetManager(Config.CRM_SPREADSHEET_PATH)
        self.caller = CallHandler(Config.VAPI_API_KEY)
        self.summarizer = CallSummarizer(Config.GROQ_API_KEY)
        print("CRM Caller initialization complete")

    def handle_ticket_creation(self, customer_id: str, summary: dict) -> bool:
        """Evaluate call summary and create a ticket if needed.
        
        Args:
            customer_id (str): The customer's ID
            summary (dict): The call summary
            
        Returns:
            bool: True if a ticket was created, False otherwise
        """
        print(f"\n=== Processing ticket creation for customer {customer_id} ===")
        
        # Check if a ticket is already open
        if self.crm.has_open_ticket(customer_id):
            print(f"⚠️ Customer {customer_id} already has an open ticket")
            return False

        # Create a ticket if there are action items or urgent follow-up needed
        print(f"Analyzing call summary for customer {customer_id}...")
        if summary['action_items'] or 'urgent' in summary['follow_up'].lower():
            print(f"📝 Creating ticket for customer {customer_id}")
            self.crm.create_ticket(customer_id, summary)
            print(f"✅ Ticket created successfully for customer {customer_id}")
            return True
            
        print(f"ℹ️ No ticket required for customer {customer_id}")
        return False

    def process_customer(self, customer: dict) -> None:
        """Process a single customer with the updated call handling.
        
        This method orchestrates the entire customer interaction process:
        making the call, getting the transcript, and handling follow-up.
        
        Args:
            customer (dict): Customer information including phone number
        """
        print(f"\n=== Starting customer process for {customer['phone_number']} ===")
        try:
            # Initiate the call
            print(f"📞 Initiating call to {customer['phone_number']}...")
            call_response = self.caller.make_call(customer['phone_number'])
            call_id = call_response['call_id']
            print(f"✅ Call initiated successfully. Call ID: {call_id}")
            
            try:
                # Get call details with a 5-minute timeout
                print(f"⏳ Waiting for call details (timeout: 300s)...")
                call_details = self.caller.get_call_details(call_id, max_wait_seconds=300)
                print("✅ Call details retrieved successfully")
                
                if call_details['status'] == 'completed':
                    # Generate summary using Groq
                    summary = self.summarizer.summarize_call(call_details['transcript'])
                    
                    # Handle ticket creation if needed
                    ticket_created = self.handle_ticket_creation(
                        customer['customer_id'], 
                        summary
                    )
                    
                    # Update contact record
                    self.crm.update_last_contact(customer['customer_id'])
                    
                    print(f"Successfully processed customer {customer['customer_id']}")
                    if ticket_created:
                        print(f"Created follow-up ticket for customer {customer['customer_id']}")
                
                else:
                    print(f"Call failed for customer {customer['customer_id']}")
                    
            finally:
                # Ensure we always stop the call
                self.caller.stop_call()
                
        except Exception as e:
            print(f"Error processing customer {customer['customer_id']}: {str(e)}")

def run():
    print("\n====================================")
    print("🤖 Starting CRM Caller Application 🤖")
    print("====================================\n")
    
    start_time = time.time()
    try:
        caller = CRMCaller()
        customers = caller.crm.get_customers()
        
        print(f"📋 Found {len(customers)} customers to process")
        
        for i, customer in enumerate(customers, 1):
            print(f"\n[{i}/{len(customers)}] Processing customer...")
            caller.process_customer(customer)
            
        elapsed_time = time.time() - start_time
        print(f"\n✅ Process completed successfully!")
        print(f"⏱️ Total execution time: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        raise
    finally:
        print("\n====================================")
        print("🔚 CRM Caller Application Finished 🔚")
        print("====================================\n")

if __name__ == "__main__":
    run()