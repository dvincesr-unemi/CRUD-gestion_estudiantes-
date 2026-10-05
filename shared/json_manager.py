import json
import os

class GestorJSON:
    """
    Clase encargada de manejar la persistencia de datos.
    Lee y guarda una lista de diccionarios en un archivo JSON.
    """

    def __init__(self, ruta: str) -> None:
        """
        Constructor de la clase. Configura la ruta del archivo y crea el 
        directorio contenedor si este no existe.
        
        Args:
            ruta (str): La ubicación del archivo JSON (ej. 'data/clientes.json').
            
        Returns:
            None 
        """
        self.ruta = ruta
        
        # Extrae solo la parte de la carpeta de la ruta dada. 
        # Si ruta es 'data/clientes.json', carpeta será 'data'.
        carpeta = os.path.dirname(ruta)
        
        # Si la ruta tiene una carpeta especificada y esta no existe en el sistema, la crea.
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self) -> list:
        """
        Abre el archivo JSON, lee su contenido y lo devuelve como una lista de Python.
        
        Args:
            Ninguno.
            
        Returns:
            list: Una lista de datos (generalmente diccionarios). Si el archivo
                  no existe, está corrupto o vacío, garantiza devolver una lista vacía [].
        """
        # Validamos primero si el archivo existe. Si no, devolvemos una lista vacía 
        # para que el programa pueda empezar sin errores la primera vez.
        if not os.path.exists(self.ruta):
            return []
            
        try:
            # Usamos 'with' para que Python cierre el archivo automáticamente al terminar.
            # encoding="utf-8" es crucial en español para leer bien las tildes y eñes.
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            
            # Defensa adicional: Si por error el JSON tiene un diccionario suelto en vez 
            # de una lista, lo descartamos y devolvemos [] para no romper la app.
            return datos if isinstance(datos, list) else []
            
        except (json.JSONDecodeError, OSError):
            # Capturamos errores concretos (JSON corrupto o error de lectura de disco)
            return []

    def guardar(self, datos: list) -> bool:
        """
        Sobrescribe el archivo JSON con los datos proporcionados.
        
        Args:
            datos (list): La lista (usualmente de diccionarios) que se desea guardar.
            
        Returns:
            bool: True si la operación de escritura fue exitosa, False en caso de error.
        """
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                # ensure_ascii=False evita que las letras como la 'ñ' se guarden como '\u00f1'
                # indent=2 formatea el archivo para que sea legible por humanos (bonito)
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
            
        except (TypeError, OSError):
            # TypeError saltará si intentamos guardar un tipo de dato que JSON no 
            # entiende (por ejemplo, una clase instanciada sin convertirla a diccionario).
            return False