# Sistema de Agentes de Investigación Financiera

Un sistema basado en CrewAI para la investigación y análisis automatizado del mercado financiero.

## Descripción General

Este proyecto implementa un sistema multiagente para llevar a cabo investigaciones en el mercado financiero:
- **Agente Investigador:** Recopila datos del mercado utilizando diversas herramientas de scraping.
- **Agente Analista:** Interpreta los datos recopilados e identifica ideas clave.
- **Agente Redactor:** Crea informes completos en formato markdown.

## Configuración

1. Clona el repositorio.
2. Crea un archivo .env con tus claves de API:
   ```
   SERPER_API_KEY=tu_clave_aquí
   TAVILY_API_KEY=tu_clave_aquí
   APIFY_API_KEY=tu_clave_aquí
   OPENAI_API_KEY=tu_clave_aquí
   ```

## Uso
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python financial_research/main.py

## Estructura del proyecto

financial_research/
├── agents/ # Agent definitions
├── tools/ # Scraping tools
├── config/ # Configuration settings
├── main.py # Main application
└── requirements.txt
