import pandas as pd
from typing import List, Dict
from datetime import datetime

class SpreadsheetManager:
    def __init__(self, spreadsheet_path: str):
        """Initialize the spreadsheet manager with the path to the CRM spreadsheet.
        
        Args:
            spreadsheet_path (str): Path to the Excel/CSV file containing customer data
        """
        self.spreadsheet_path = spreadsheet_path
        self.data = None
        self._load_data()

    def _load_data(self) -> None:
        """Load the spreadsheet data into a pandas DataFrame and ensure all required columns exist."""
        try:
            # Try Excel format first
            self.data = pd.read_excel(self.spreadsheet_path)
        except Exception:
            # Fall back to CSV if Excel fails
            self.data = pd.read_csv(self.spreadsheet_path)
        
        # Ensure required columns exist
        required_columns = ['customer_id', 'phone_number', 'last_contact', 'ticket_status']
        
        # Add missing columns with default values
        for column in required_columns:
            if column not in self.data.columns:
                if column == 'ticket_status':
                    self.data[column] = 'none'  # Default ticket status
                elif column == 'last_contact':
                    self.data[column] = None
                else:
                    raise ValueError(f"Missing required column: {column}")
        
        # Save the updated structure if we added any columns
        self._save_data()

    def get_customers(self) -> List[Dict]:
        """
        Retrieve customer data from spreadsheet.
        
        Returns:
            List[Dict]: List of customer records with required fields
        """
        try:
            # Read spreadsheet into DataFrame
            df = pd.read_excel(self.spreadsheet_path)
            
            # Convert DataFrame to list of dictionaries
            customers = df.to_dict('records')
            
            # Validate required fields
            required_fields = ['customer_id', 'phone_number']
            for customer in customers:
                missing_fields = [field for field in required_fields if field not in customer]
                if missing_fields:
                    raise ValueError(f"Missing required fields: {missing_fields}")
            
            return customers
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Customer spreadsheet not found at {self.spreadsheet_path}")
        except Exception as e:
            raise Exception(f"Error reading customer data: {str(e)}")

    def create_ticket(self, customer_id: str, summary: Dict) -> None:
        """Mark a customer as having an open ticket and store the ticket details.
        
        Args:
            customer_id (str): The ID of the customer
            summary (Dict): The call summary containing key points and action items
        """
        mask = self.data['customer_id'] == customer_id
        
        # Update ticket status
        self.data.loc[mask, 'ticket_status'] = 'open'
        
        # If we don't have these columns, create them
        if 'ticket_details' not in self.data.columns:
            self.data['ticket_details'] = None
        if 'ticket_created_date' not in self.data.columns:
            self.data['ticket_created_date'] = None
        
        # Store ticket details as a formatted string
        ticket_details = (
            f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Key Points: {'; '.join(summary['key_points'])}\n"
            f"Action Items: {'; '.join(summary['action_items'])}\n"
            f"Follow-up: {summary['follow_up']}"
        )
        
        self.data.loc[mask, 'ticket_details'] = ticket_details
        self.data.loc[mask, 'ticket_created_date'] = datetime.now()
        
        # Save the changes
        self._save_data()

    def has_open_ticket(self, customer_id: str) -> bool:
        """Check if a customer has an open ticket.
        
        Args:
            customer_id (str): The ID of the customer to check
            
        Returns:
            bool: True if the customer has an open ticket, False otherwise
        """
        mask = self.data['customer_id'] == customer_id
        if not mask.any():
            return False
        return self.data.loc[mask, 'ticket_status'].iloc[0] == 'open'

    def get_customers_to_call(self, days_since_last_contact: int = 30) -> List[Dict]:
        """Get a list of customers who haven't been contacted in the specified number of days.
        
        Args:
            days_since_last_contact (int): Number of days since last contact
            
        Returns:
            List[Dict]: List of customer records
        """
        today = datetime.now()
        self.data['last_contact'] = pd.to_datetime(self.data['last_contact'])
        
        # Filter customers based on last contact date
        needs_contact = self.data[
            (today - self.data['last_contact']).dt.days >= days_since_last_contact
        ]
        
        return needs_contact.to_dict('records')

    def update_last_contact(self, customer_id: str) -> None:
        """Update the last contact date for a customer.
        
        Args:
            customer_id (str): The ID of the customer to update
        """
        mask = self.data['customer_id'] == customer_id
        self.data.loc[mask, 'last_contact'] = datetime.now()
        self._save_data()

    def _save_data(self) -> None:
        """Save the updated data back to the spreadsheet."""
        if self.spreadsheet_path.endswith('.xlsx'):
            self.data.to_excel(self.spreadsheet_path, index=False)
        else:
            self.data.to_csv(self.spreadsheet_path, index=False)