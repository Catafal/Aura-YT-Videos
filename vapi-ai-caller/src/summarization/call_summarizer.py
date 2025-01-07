import groq
from typing import Dict, Optional

class CallSummarizer:
    def __init__(self, api_key: str):
        """Initialize the call summarizer with the Groq API key.
        
        Args:
            api_key (str): Groq API key for authentication
        """
        self.client = groq.Client(api_key=api_key)

    def summarize_call(self, transcript: str) -> Dict:
        """Generate a summary of the call using Groq's LLM.
        
        Args:
            transcript (str): The call transcript to summarize
            
        Returns:
            Dict: Summary containing key points, action items, and sentiment
        """
        prompt = f"""
        Please analyze this customer call transcript and provide a structured summary:
        
        Transcript:
        {transcript}
        
        Please provide:
        1. Key points discussed
        2. Action items
        3. Customer sentiment
        4. Follow-up recommendations
        """

        response = self.client.chat.completions.create(
            model="llama3.3",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes customer service calls."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return self._parse_summary(response.choices[0].message.content)

    def _parse_summary(self, summary_text: str) -> Dict:
        """Parse the raw summary text into a structured format.
        
        Args:
            summary_text (str): Raw summary text from Groq
            
        Returns:
            Dict: Structured summary with key sections
        """
        # This is a simple implementation
        sections = summary_text.split('\n\n')
        summary = {
            'key_points': [],
            'action_items': [],
            'sentiment': '',
            'follow_up': ''
        }
        
        current_section = None
        for section in sections:
            if 'Key points' in section:
                current_section = 'key_points'
            elif 'Action items' in section:
                current_section = 'action_items'
            elif 'Customer sentiment' in section:
                current_section = 'sentiment'
            elif 'Follow-up' in section:
                current_section = 'follow_up'
            
            if current_section:
                if isinstance(summary[current_section], list):
                    points = [p.strip('- ') for p in section.split('\n')[1:] if p.strip()]
                    summary[current_section].extend(points)
                else:
                    summary[current_section] = section.split('\n', 1)[1].strip()

        return summary