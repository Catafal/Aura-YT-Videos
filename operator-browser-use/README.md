# Sistema Multi-Agente para Reservas de Hotel

## Descripción
Este proyecto implementa un sistema automatizado de búsqueda y reserva de hoteles utilizando múltiples agentes inteligentes. El sistema es capaz de buscar, comparar y reservar hoteles en diferentes plataformas de manera simultánea, encontrando las mejores ofertas para el usuario.

## Características Principales
- 🤖 Sistema multi-agente usando CrewAI
- 🌐 Búsqueda simultánea en múltiples sitios web
- 💰 Comparación automática de precios
- 📝 Almacenamiento local de datos de usuario
- 🔄 Proceso automatizado de reserva

## Tecnologías Utilizadas
- CrewAI para la orquestación de agentes
- Browser-use para interacción web
- Modelo Janus-Pro-7B para toma de decisiones
- Python 3.8+

## Estructura del Proyecto
src/
├── agents/
│ ├── init.py
│ ├── search_agent.py
│ ├── comparison_agent.py
│ ├── booking_agent.py
│ └── data_agent.py
├── tools/
│ ├── init.py
│ ├── browser_tools.py
│ └── data_tools.py
├── config/
│ └── config.py
└── main.py

## Instalación

1. Clonar el repositorio:
    bash
    git clone [https://github.com/jordicatafal/Aura-YT-Videos/operator-deepseek]
    cd src
2. Instalar dependencias:
    bash
    pip install -r requirements.txt

3. Configurar variables de entorno:
    .env
    OPENAI_API_KEY=tu_api_key_de_openai


## Uso

1. Ejecutar el sistema:
    python main.py

########################################################

## Agentes del Sistema

### 🔍 Agente de Búsqueda
- Busca hoteles en múltiples plataformas
- Recopila información detallada de cada opción

### 📊 Agente de Comparación
- Analiza y compara precios entre diferentes sitios
- Evalúa la mejor relación calidad-precio

### 📝 Agente de Reserva
- Gestiona el proceso de reserva
- Completa formularios automáticamente

### 💾 Agente de Datos
- Gestiona el almacenamiento de datos de usuario
- Mantiene la información actualizada

## Almacenamiento de Datos
Los datos del usuario se almacenan localmente en formato JSON para futuras reservas, incluyendo:
- Información personal
- Preferencias de hotel
- Historial de reservas

## Licencia
Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto
Jordi Catafal - jordi@aurasyst.com
URL del proyecto: [https://github.com/jordicatafal/Aura-YT-Videos/operator-deepseek]
