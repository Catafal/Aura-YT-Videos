from crewai.tools import tool
import time

class UtilityTools:
    @staticmethod
    @tool("Esperar cierta cantidad de tiempo")
    def wait(mins: int) -> str:
        """Esperar cierta cantidad de tiempo"""
        duration_in_seconds = mins * 60
        time.sleep(duration_in_seconds)
        print(f"¡Genial, has esperado {mins} minutos! Ahora continúa con tu tarea.")
        return f"¡Genial, has esperado {mins} minutos! Ahora continúa con tu tarea."