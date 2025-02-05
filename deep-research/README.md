# Financial Research Agent System

A CrewAI-based system for automated financial market research and analysis.

## Overview

This project implements a multi-agent system for conducting financial market research:
- Researcher Agent: Gathers market data using various scraping tools
- Analyst Agent: Interprets the gathered data and identifies key insights
- Writer Agent: Creates comprehensive markdown reports

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   SERPER_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   APIFY_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   ```

## Usage


## Project Structure

financial_research/
├── agents/ # Agent definitions
├── tools/ # Scraping tools
├── config/ # Configuration settings
├── main.py # Main application
└── requirements.txt