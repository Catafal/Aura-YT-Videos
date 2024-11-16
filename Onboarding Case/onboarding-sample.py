# pip -m venv venv (para crear un entorno virtual)
# source venv/bin/activate (para activar el entorno virtual)
# pip install firecrawl-py groq (para instalar dependencias)
# python3 onboarding-sample.py (para ejecutar el script)

import json
import os
from typing import List, Dict
from collections import defaultdict
from firecrawl import FirecrawlApp
from groq import Groq
from datetime import datetime
from dotenv import load_dotenv

class AnalizadorWeb:
    def __init__(self, clave_api_firecrawl: str, clave_api_groq: str):
        """
        Crea una instancia de FirecrawlApp y Groq con la clave API proporcionada.
        
        Es como preparar todo lo necesario antes de empezar a trabajar. 

        Por ejemplo:

        - Iniciar un coche: primero introduces la llave y enciendes el motor
        
        """
        self.firecrawl = FirecrawlApp(api_key=clave_api_firecrawl)
        self.groq_cliente = Groq(api_key=clave_api_groq)
        self.contenido_extraido = []
        
    def _generar_esquema_extraccion(self) -> str:
        """Definimos exactamente qué información necesitas recopilar"""
        esquema = {
        "informacion_empresa": {
            "nombre": "str",
            "descripcion": "str",
            "sector": "str",
            "año_fundacion": "str"
        },
        "contacto": {
            "email": "str",
            "telefono": "str",
            "redes_sociales": {
                "linkedin": "str",
                "twitter": "str",
                "instagram": "str"
            }
        },
        "ubicaciones": [{
            "tipo": "str",  
            "direccion": {
                "calle": "str",
                "ciudad": "str",
                "provincia": "str",
                "codigo_postal": "str"
            },
            "horario_atencion": [{
                "dia": "str",
                "hora_apertura": "str",
                "hora_cierre": "str"
            }]
        }],
        "informacion_adicional": "str"  # Campo libre para que el modelo incluya cualquier información relevante adicional
    }
        return json.dumps(esquema, indent=2)

    def _obtener_prompt_sistema(self) -> str:
        """
        Damos instrucciones al modelo de Groq sobre qué queremos que haga.
        Usamos JSON, que es un formato para estructurar datos. 
        Es fácil para nosotros de leer y escribir, y también es fácil para las máquinas.

        """
        return f"""
        Eres un experto en extraer datos de contenido web y convertirlos a formato JSON. 
        La respuesta debe incluir las siguientes propiedades en el JSON:
        
        {self._generar_esquema_extraccion()}

        Por favor, proporciona la información extraída en un formato que coincida con este esquema JSON.
        """

    def extraer_url_individual(self, url: str) -> None:
        """
        Extrae contenido de una única web y lo guarda usando markdown.
        Que es un formato de texto plano fácil de leer y escribir. Sin nada de HTML (código).

        """
        try:
            respuesta_extraccion = self.firecrawl.scrape_url(
                url,
                params={'formats': ['markdown']}
            )
            self.contenido_extraido.append(respuesta_extraccion["markdown"])
            print(f"Extracción exitosa de {url}")
        except Exception as e:
            print(f"Error al extraer {url}: {str(e)}")

    def rastrear_sitio_web(self, url_dominio: str, limite: int = 2) -> None:
        """
        Rastrea todo un sitio web comenzando desde la URL del dominio.
        Puede rastrear múltiples páginas y extraer contenido de cada una.
        Por lo tanto, todas las subpáginas de un sitio web serán rastreadas.

        """
        try:
            respuesta_rastreo = self.firecrawl.crawl_url(
                url_dominio,
                params={
                    'limit': limite,
                    'scrapeOptions': {'formats': ['markdown']}
                }
            )
            
            self.contenido_extraido.extend(
                sitio["markdown"] for sitio in respuesta_rastreo["data"]
            )
            print(f"Rastreo exitoso de {url_dominio} con límite {limite} páginas")
        except Exception as e:
            print(f"Error al rastrear {url_dominio}: {str(e)}")

    def extraer_informacion(self, contenido: str) -> Dict:
        """
        Extrae información de un contenido individual usando Groq.
        Es como tener un analista experto que revisa lo extraído y resalta la información importante.

        """
        try:
            respuesta = self.groq_cliente.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": self._obtener_prompt_sistema()
                    },
                    {
                        "role": "user",
                        "content": contenido
                    }
                ],
                temperature=0,
                max_tokens=8000,
                top_p=1,
                stream=False,
                response_format={"type": "json_object"},
                stop=None,
            )
            
            info_extraida = json.loads(respuesta.choices[0].message.content)
            return info_extraida
        except Exception as e:
            print(f"Error durante la extracción: {str(e)}")
            return {}

    def procesar_todo_contenido(self) -> Dict:
        """Procesa todo el contenido extraído y se combina."""
        contenido_extraido = []
        
        for contenido in self.contenido_extraido:
            extraido = self.extraer_informacion(contenido)
            if extraido:
                nombre_negocio = extraido.get('nombre_negocio', 'Negocio Desconocido')
                contenido_extraido.append({nombre_negocio: extraido})
        
        return self._combinar_datos_extraidos(contenido_extraido)

    def _combinar_datos_extraidos(self, contenido_extraido: List[Dict]) -> Dict:
        """
        Combina todos los datos extraídos en un único diccionario (tipo de estructura de datos).
        Por lo tanto simplemente, organizamos toda la información en un solo lugar. 

        """
        combinado = defaultdict(lambda: {
        'informacion_empresa': {
            'nombre': '',
            'descripcion': '',
            'sector': '',
            'año_fundacion': ''
        },
        'contacto': {
            'email': '',
            'telefono': '',
            'redes_sociales': {
                'linkedin': '',
                'twitter': '',
                'instagram': ''
            }
        },
        'ubicaciones': [{
            'tipo': '',
            'direccion': {
                'calle': '',
                'ciudad': '',
                'provincia': '',
                'codigo_postal': ''
            },
            'horario_atencion': []
        }],
        'informacion_adicional': ''
    })

        for diccionario_contenido in contenido_extraido:
            for nombre_empresa, detalles in diccionario_contenido.items():
                
                if detalles.get('informacion_empresa'):
                    for campo in ['nombre', 'descripcion', 'sector', 'año_fundacion']:
                        if detalles['informacion_empresa'].get(campo):
                            combinado[nombre_empresa]['informacion_empresa'][campo] = detalles['informacion_empresa'][campo]

                
                if detalles.get('contacto'):
                    for campo in ['email', 'telefono']:
                        if detalles['contacto'].get(campo):
                            combinado[nombre_empresa]['contacto'][campo] = detalles['contacto'][campo]
                    
                   
                    if detalles['contacto'].get('redes_sociales'):
                        for red in ['linkedin', 'twitter', 'instagram']:
                            if detalles['contacto']['redes_sociales'].get(red):
                                combinado[nombre_empresa]['contacto']['redes_sociales'][red] = \
                                    detalles['contacto']['redes_sociales'][red]

               
                if detalles.get('ubicaciones'):
                   
                    ubicaciones_existentes = combinado[nombre_empresa]['ubicaciones']
                    for nueva_ubicacion in detalles['ubicaciones']:
                       
                        ubicacion_encontrada = False
                        for i, ubicacion_existente in enumerate(ubicaciones_existentes):
                            if (ubicacion_existente['direccion']['calle'] == nueva_ubicacion['direccion']['calle'] and
                                ubicacion_existente['direccion']['ciudad'] == nueva_ubicacion['direccion']['ciudad']):
                                
                                ubicaciones_existentes[i].update(nueva_ubicacion)
                                ubicacion_encontrada = True
                                break
                        
                        if not ubicacion_encontrada:
                            
                            ubicaciones_existentes.append(nueva_ubicacion)

                
                if detalles.get('informacion_adicional'):
                    if combinado[nombre_empresa]['informacion_adicional']:
                    
                        combinado[nombre_empresa]['informacion_adicional'] += "\n" + detalles['informacion_adicional']
                    else:
                        combinado[nombre_empresa]['informacion_adicional'] = detalles['informacion_adicional']

        return dict(combinado)

    def guardar_resultados(self, datos: Dict, directorio_salida: str = "resultados_analisis") -> str:
        """Guarda los resultados del análisis en un archivo JSON."""
        os.makedirs(directorio_salida, exist_ok=True)
        marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = os.path.join(directorio_salida, f"analisis_negocio_{marca_tiempo}.json")
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        
        return nombre_archivo

def main():
    
    load_dotenv()

    
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    if not FIRECRAWL_API_KEY or not GROQ_API_KEY:
        raise ValueError("Por favor, configura las variables de entorno CLAVE_FIRECRAWL y CLAVE_GROQ")

   
    analizador = AnalizadorWeb(FIRECRAWL_API_KEY, GROQ_API_KEY)

    
    url_objetivo = "https://www.elnacionalbcn.com"
    
    
    analizador.extraer_url_individual(url_objetivo)
    analizador.rastrear_sitio_web(url_objetivo, limite=3)
    
    
    resultados = analizador.procesar_todo_contenido()
    
    
    archivo_salida = analizador.guardar_resultados(resultados)
    print(f"Resultados del análisis guardados en: {archivo_salida}")
    
    
    print("\nResumen del Análisis:")
    for nombre_negocio, detalles in resultados.items():
        print(f"\nNegocio: {nombre_negocio}")
        print(f"Dirección: {detalles['direccion_negocio']['calle']}, "
              f"{detalles['direccion_negocio']['ciudad']}, "
              f"{detalles['direccion_negocio']['codigo_postal']}")
        print(f"Teléfono: {detalles['telefono']}")
        print(f"Número de elementos en el menú: {len(detalles['elementos_menu'])}")
        print(f"Entradas de horarios: {len(detalles['horario_apertura'])}")

if __name__ == "__main__":
    main()