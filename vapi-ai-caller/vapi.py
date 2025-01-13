import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.vapi.ai/call/phone"
customer_name = "Jordi"
sales_name = "Diego"


payload = {
    "phoneNumberId": os.getenv("VAPI_PHONE_NUMBER_ID"),
    "assistantId": os.getenv("VAPI_ASSISTANT_ID"),
    "customer": {"number": os.getenv("PHONE_CUSTOMER"), "name": "Jordi"},
}


headers = {
    "Authorization": f"Bearer {os.getenv('VAPI_API_KEY_PRIVATE')}",
    "Content-Type": "application/json",
}


try:
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
except Exception as e:
    print(f"Error making call: {str(e)}")